"use client";

// Mappa illustrata navigabile dell'Isola dei Tre Venti.
// Porting del vecchio `catalogo_web/mappa_isola.js` come Client Component.
//
// Strategia:
//  - sfondo: illustrazione "isola_base_v1.jpg" (acquerello, no edifici)
//  - sopra: edifici/luoghi posizionati come slot derivati dal geojson canonico
//  - per ogni slot proviamo a caricare l'asset 3D PNG. Se manca → placeholder
//    cerchio tratteggiato. Click → /catalogo/<id> via Next router.
//
// Asset/geojson sono serviti dal CDN statico esistente (`IMAGE_BASE` in
// `lib/image-url`). Il vecchio path relativo `../cartografia/...` qui diventa
// `cartografia/...` (root del repo).

import * as React from "react";
import { useRouter } from "next/navigation";

import { imageUrl } from "@/lib/image-url";

const MAPPA_CONFIG = {
  base_image: "cartografia/assets_mappa/_base/isola_base_v1.jpg",
  geojson_url: "cartografia/geo/island.geojson",
  assets_dir: "cartografia/assets_mappa/",
  image_w: 1120,
  image_h: 912,
  bbox_geo: {
    lon_min: 17.945,
    lon_max: 18.06,
    lat_min: 34.46,
    lat_max: 34.535,
  },
  slot_types: new Set([
    "building",
    "burrow",
    "cave",
    "pier",
    "landmark",
    "water_pool",
    "tree",
    "square",
  ]),
  slot_size_default: 60,
  large_landmarks: new Set([
    "albero_vecchio",
    "due_massi",
    "roccia_alta",
    "noce_della_scuola",
  ]),
} as const;

interface Slot {
  id: string;
  name: string;
  type: string;
  status: string;
  x: number;
  y: number;
  size: number;
  asset_url: string;
  has_asset: boolean | null; // null = unknown
}

interface GeoFeatureProperties {
  id?: string;
  name?: string;
  type?: string;
  category?: string;
  quarter?: string;
  status?: string;
  aggregate?: boolean;
}

interface GeoFeature {
  type: string;
  geometry: {
    type: string;
    coordinates: unknown;
  } | null;
  properties: GeoFeatureProperties;
}

interface GeoJSON {
  features: GeoFeature[];
}

function featureCenter(f: GeoFeature): [number, number] | null {
  const g = f.geometry;
  if (!g) return null;
  if (g.type === "Point") return g.coordinates as [number, number];
  if (g.type === "Polygon") {
    const ring = (g.coordinates as number[][][])[0];
    let cx = 0;
    let cy = 0;
    for (const c of ring) {
      cx += c[0];
      cy += c[1];
    }
    return [cx / ring.length, cy / ring.length];
  }
  if (g.type === "MultiPoint") {
    const pts = g.coordinates as number[][];
    let cx = 0;
    let cy = 0;
    for (const c of pts) {
      cx += c[0];
      cy += c[1];
    }
    return [cx / pts.length, cy / pts.length];
  }
  return null;
}

function lonLatToViewBox(lon: number, lat: number): [number, number] {
  const { lon_min, lon_max, lat_min, lat_max } = MAPPA_CONFIG.bbox_geo;
  const W = MAPPA_CONFIG.image_w;
  const H = MAPPA_CONFIG.image_h;
  const x = ((lon - lon_min) / (lon_max - lon_min)) * W;
  const y = ((lat_max - lat) / (lat_max - lat_min)) * H;
  return [x, y];
}

function slotSizeFor(props: GeoFeatureProperties): number {
  if (props.id && MAPPA_CONFIG.large_landmarks.has(props.id)) return 100;
  if (props.type === "square") return 90;
  if (props.type === "landmark") return 50;
  if (props.type === "tree") return 80;
  if (props.type === "burrow" || props.type === "cave") return 55;
  return MAPPA_CONFIG.slot_size_default;
}

function extractSlotsFromGeoJSON(geojson: GeoJSON): Slot[] {
  const slots: Slot[] = [];
  for (const f of geojson.features ?? []) {
    const p = f.properties ?? {};
    const t = p.type;
    if (!t || !MAPPA_CONFIG.slot_types.has(t)) continue;
    if (p.aggregate) continue;
    const center = featureCenter(f);
    if (!center) continue;
    const id = p.id;
    if (!id) continue;
    const [lon, lat] = center;
    const [x, y] = lonLatToViewBox(lon, lat);
    slots.push({
      id,
      name: p.name || id,
      type: t,
      status: p.status || "provvisorio",
      x,
      y,
      size: slotSizeFor(p),
      asset_url: imageUrl(`${MAPPA_CONFIG.assets_dir}${id}.png`),
      has_asset: null,
    });
  }
  return slots;
}

const STATUS_COLOR: Record<string, string> = {
  canonico: "#5c4a28",
  provvisorio: "#a07020",
  stub: "#a04040",
};

export function MappaIsola() {
  const router = useRouter();
  const [slots, setSlots] = React.useState<Slot[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    let cancelled = false;
    async function run() {
      try {
        const r = await fetch(imageUrl(MAPPA_CONFIG.geojson_url));
        if (!r.ok) throw new Error(`geojson HTTP ${r.status}`);
        const geo = (await r.json()) as GeoJSON;
        if (cancelled) return;
        const initial = extractSlotsFromGeoJSON(geo);
        setSlots(initial);
        setLoading(false);

        // HEAD-check assets in parallelo (best effort).
        const checked = await Promise.all(
          initial.map(async (s) => {
            try {
              const head = await fetch(s.asset_url, { method: "HEAD" });
              return { ...s, has_asset: head.ok };
            } catch {
              return { ...s, has_asset: false };
            }
          }),
        );
        if (!cancelled) setSlots(checked);
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : String(err));
          setLoading(false);
        }
      }
    }
    void run();
    return () => {
      cancelled = true;
    };
  }, []);

  if (error) {
    return (
      <div className="rounded-md border border-rule-soft bg-paper-soft p-6">
        <h2 className="font-serif text-lg font-semibold text-ink">
          Errore caricamento mappa
        </h2>
        <p className="font-serif italic text-ink-soft mt-2">{error}</p>
        <p className="font-mono text-xs text-ink-faint mt-2">
          Verifica che il file <code>cartografia/geo/island.geojson</code> sia
          raggiungibile dal CDN.
        </p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="rounded-md border border-rule-soft bg-paper-soft p-6">
        <p className="font-serif italic text-ink-soft">Caricamento mappa…</p>
      </div>
    );
  }

  const total = slots.length;
  const placed = slots.filter((s) => s.has_asset).length;

  function openEntity(id: string) {
    router.push(`/catalogo/${id}`);
  }

  return (
    <div className="space-y-4">
      <p className="font-mono text-sm text-ink-soft">
        {placed}/{total} edifici con asset 3D ·{" "}
        <span className="italic">click su un punto per aprire la scheda</span>
      </p>
      <div
        className="relative overflow-hidden rounded-md border border-rule-soft bg-paper-soft shadow-[0_2px_12px_rgba(0,0,0,0.08)]"
        style={{ aspectRatio: `${MAPPA_CONFIG.image_w} / ${MAPPA_CONFIG.image_h}` }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox={`0 0 ${MAPPA_CONFIG.image_w} ${MAPPA_CONFIG.image_h}`}
          preserveAspectRatio="xMidYMid meet"
          role="img"
          aria-label="Mappa illustrata dell'Isola dei Tre Venti"
          className="block w-full h-auto select-none"
        >
          <image
            href={imageUrl(MAPPA_CONFIG.base_image)}
            x={0}
            y={0}
            width={MAPPA_CONFIG.image_w}
            height={MAPPA_CONFIG.image_h}
            preserveAspectRatio="none"
          />
          <g>
            {slots.map((s) => (
              <SlotMarker key={s.id} slot={s} onClick={() => openEntity(s.id)} />
            ))}
          </g>
        </svg>
      </div>
      <details className="rounded-md border border-rule-soft bg-paper-soft px-4 py-3 text-sm text-ink-soft">
        <summary className="cursor-pointer font-semibold text-ink">
          Legenda &amp; come funziona
        </summary>
        <ul className="mt-2 list-disc pl-5 space-y-1.5">
          <li>
            I cerchi tratteggiati sono <strong>slot vuoti</strong>: posizione
            canonica ma asset 3D non ancora generato.
          </li>
          <li>Gli edifici 3D sono PNG sovrapposti all&apos;illustrazione base.</li>
          <li>
            La posizione di ogni slot deriva dal centroide della feature in{" "}
            <code className="bg-rule-soft/40 rounded px-1">
              cartografia/geo/island.geojson
            </code>
            .
          </li>
          <li>
            Click su un punto → apre la scheda corrispondente nel catalogo.
          </li>
        </ul>
      </details>
    </div>
  );
}

function SlotMarker({ slot, onClick }: { slot: Slot; onClick: () => void }) {
  const half = slot.size / 2;
  const labelY = slot.has_asset ? slot.y + 10 : slot.y + slot.size / 3 + 14;

  return (
    <g
      tabIndex={0}
      role="button"
      aria-label={slot.has_asset ? slot.name : `${slot.name} (slot vuoto)`}
      onClick={onClick}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          onClick();
        }
      }}
      className="cursor-pointer transition-[filter] duration-150 hover:[filter:drop-shadow(0_2px_6px_rgba(0,0,0,0.35))] focus:outline-none"
    >
      <title>
        {slot.name} ({slot.id})
      </title>
      {slot.has_asset ? (
        <image
          href={slot.asset_url}
          x={slot.x - half}
          y={slot.y - slot.size * 0.85}
          width={slot.size}
          height={slot.size}
          preserveAspectRatio="xMidYMax meet"
        />
      ) : (
        <>
          <circle
            cx={slot.x}
            cy={slot.y}
            r={slot.size / 3}
            fill="rgba(255,255,255,0.55)"
            stroke={STATUS_COLOR[slot.status] ?? "#666"}
            strokeWidth={1.6}
            strokeDasharray="4 3"
          />
          <circle
            cx={slot.x}
            cy={slot.y}
            r={2.5}
            fill={STATUS_COLOR[slot.status] ?? "#666"}
          />
        </>
      )}
      <text
        x={slot.x}
        y={labelY}
        textAnchor="middle"
        className="pointer-events-none select-none"
        style={{
          fontFamily: "var(--font-fraunces), Georgia, serif",
          fontSize: 13,
          fontWeight: 500,
          fill: "#3a2f1c",
          paintOrder: "stroke fill",
          stroke: "rgba(255, 248, 230, 0.85)",
          strokeWidth: 3,
          strokeLinejoin: "round",
        }}
      >
        {slot.name}
      </text>
    </g>
  );
}
