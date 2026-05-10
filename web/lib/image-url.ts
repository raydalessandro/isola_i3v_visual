// Client-safe helpers per costruire URL pubblici delle immagini catalogo.
// Tenuti separati da `lib/data.ts` (che usa fs/promises ed è server-only).
//
// Le immagini vengono servite dal deploy statico esistente del catalogo
// finché non faremo il cutover. Il path `relPath` arriva dal JSON ed è
// nella forma "visual/<categoria>/.../immagini/<file>.jpg".
//
// Cutover: basta cambiare NEXT_PUBLIC_IMAGE_BASE.

export const IMAGE_BASE: string =
  (typeof process !== "undefined" &&
    process.env &&
    (process.env.NEXT_PUBLIC_IMAGE_BASE as string | undefined)) ||
  "https://catalogoisola.vercel.app";

export function imageUrl(relPath: string): string {
  const base = IMAGE_BASE.replace(/\/+$/, "");
  const normalized = relPath.startsWith("/") ? relPath : "/" + relPath;
  return base + normalized;
}
