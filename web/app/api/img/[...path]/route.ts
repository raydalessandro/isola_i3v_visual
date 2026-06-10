// Proxy immagini same-origin — WI-3 catalogo v2.
//
// Perché esiste: l'attributo `download` di <a> NON funziona per risorse
// cross-origin (è una restrizione standard del browser, ignora il valore).
// Mettere il proxy davanti rende il download di IMAGE_BASE possibile, e
// prepara il cutover: quando il dominio del catalogo cambia, basta
// aggiornare IMAGE_BASE.
//
// Sicurezza:
//   - whitelist sul prefisso `visual/`: niente traversal, niente path
//     verso altri endpoint del dominio sorgente;
//   - estensioni immagine fissate (no eseguibili, no HTML);
//   - tutto in lettura, niente effetti collaterali.
//
// Performance: caching aggressivo (`immutable`, 1 anno) — i file hanno
// nomi canonici versionati (`<id>_canonica_v1_<vista>.jpg`), quindi un
// cambio = nuovo nome.

import { NextResponse } from "next/server";
import { IMAGE_BASE } from "@/lib/image-url";

// Tenuto in sync con `IMG_EXTS` di scripts/build_catalogo_web.py.
const ALLOWED_EXTENSIONS = new Set([
  "png",
  "jpg",
  "jpeg",
  "webp",
  "gif",
  "svg",
]);

const PATH_PREFIX = "visual";

interface RouteContext {
  params: Promise<{ path: string[] }>;
}

export async function GET(
  request: Request,
  { params }: RouteContext,
): Promise<Response> {
  const { path: segments } = await params;

  if (!segments || segments.length === 0) {
    return new NextResponse("missing path", { status: 400 });
  }

  // No traversal e no segmenti vuoti.
  if (segments.some((s) => s === ".." || s === "" || s.includes("/"))) {
    return new NextResponse("invalid path", { status: 400 });
  }

  // Whitelist prefisso.
  if (segments[0] !== PATH_PREFIX) {
    return new NextResponse("forbidden prefix", { status: 403 });
  }

  // Estensione consentita.
  const last = segments[segments.length - 1];
  const dot = last.lastIndexOf(".");
  const ext = dot >= 0 ? last.slice(dot + 1).toLowerCase() : "";
  if (!ALLOWED_EXTENSIONS.has(ext)) {
    return new NextResponse("unsupported extension", { status: 415 });
  }

  const url = new URL(request.url);
  const isDownload = url.searchParams.get("download") === "1";

  const upstreamUrl = `${IMAGE_BASE.replace(/\/+$/, "")}/${segments.join("/")}`;

  let upstream: Response;
  try {
    upstream = await fetch(upstreamUrl, {
      // Cache controllata da noi: header sotto.
      cache: "force-cache",
    });
  } catch {
    return new NextResponse("upstream fetch failed", { status: 502 });
  }

  if (!upstream.ok) {
    return new NextResponse(`upstream ${upstream.status}`, {
      status: upstream.status,
    });
  }

  const headers = new Headers();
  const contentType = upstream.headers.get("content-type");
  if (contentType) headers.set("content-type", contentType);
  const contentLength = upstream.headers.get("content-length");
  if (contentLength) headers.set("content-length", contentLength);

  headers.set("cache-control", "public, max-age=31536000, immutable");

  if (isDownload) {
    headers.set(
      "content-disposition",
      `attachment; filename="${sanitizeFilename(last)}"`,
    );
  }

  return new Response(upstream.body, { status: 200, headers });
}

/** Difensivo: il nome viene già da segments validati, ma toglieremo
 *  qualsiasi carattere fuori da quelli safe per il header. */
function sanitizeFilename(name: string): string {
  return name.replace(/[^a-zA-Z0-9._-]/g, "_");
}
