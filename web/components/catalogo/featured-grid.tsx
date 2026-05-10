"use client";

import * as React from "react";
import Link from "next/link";
import Image from "next/image";

import type { Entity, EntityFamiglia } from "@/lib/types";
import { FAMIGLIA_LABEL_SINGOLARE, FAMIGLIA_ORDER } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { imageUrl } from "@/lib/image-url";
import { SearchBox } from "@/components/catalogo/search-box";

interface FeaturedGridProps {
  entities: Entity[];
}

/**
 * Griglia delle entità con almeno un'immagine canonica.
 * Search filtra per nome/id/famiglia case-insensitive.
 */
export function FeaturedGrid({ entities }: FeaturedGridProps) {
  const [query, setQuery] = React.useState("");

  const sorted = React.useMemo(() => sortFeatured(entities), [entities]);
  const filtered = React.useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return sorted;
    return sorted.filter((e) => {
      const hay = [e.id, e.name, e.famiglia, e.sottotipo ?? ""]
        .join(" ")
        .toLowerCase();
      return hay.includes(q);
    });
  }, [sorted, query]);

  return (
    <section aria-label="Schede con immagini canoniche" className="space-y-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <h2 className="font-serif text-2xl font-semibold text-ink">
          Schede con immagini
        </h2>
        <SearchBox
          value={query}
          onChange={setQuery}
          placeholder="Cerca per nome o id…"
          className="w-full sm:w-72"
        />
      </div>
      {filtered.length === 0 ? (
        <p className="font-serif italic text-ink-faint">
          Nessuna scheda corrisponde a &ldquo;{query}&rdquo;.
        </p>
      ) : (
        <ul className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {filtered.map((e) => (
            <li key={e.id}>
              <FeaturedCard entity={e} />
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

function FeaturedCard({ entity }: { entity: Entity }) {
  const cover = entity.images[0];
  const url = cover ? imageUrl(cover.path) : null;
  return (
    <Link
      href={`/catalogo/${entity.id}`}
      className="group block overflow-hidden rounded-lg border border-rule-soft bg-paper-soft transition-colors hover:border-accent/40"
    >
      <div className="relative aspect-square w-full bg-rule-soft/40">
        {url ? (
          <Image
            src={url}
            alt={entity.name}
            fill
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
            className="object-cover transition-transform duration-300 group-hover:scale-[1.02]"
            loading="lazy"
            unoptimized
          />
        ) : (
          <div className="absolute inset-0 grid place-items-center text-ink-faint font-mono text-xs">
            no image
          </div>
        )}
        <div className="absolute right-2 top-2 flex flex-col items-end gap-1">
          <Badge
            variant={entity.status === "canonico" ? "canonico" : "provvisorio"}
          >
            {entity.status}
          </Badge>
          {entity.n_images > 1 && (
            <Badge variant="secondary" className="font-mono">
              {entity.n_images} img
            </Badge>
          )}
        </div>
      </div>
      <div className="p-3 space-y-1">
        <div className="flex items-center justify-between gap-2">
          <h3 className="font-serif text-base font-semibold text-ink truncate">
            {entity.name}
          </h3>
        </div>
        <div className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-wider text-ink-faint">
          <span>{FAMIGLIA_LABEL_SINGOLARE[entity.famiglia]}</span>
          {entity.sottotipo && (
            <>
              <span aria-hidden>·</span>
              <span className={cn("truncate")}>{entity.sottotipo}</span>
            </>
          )}
        </div>
      </div>
    </Link>
  );
}

function sortFeatured(entities: Entity[]): Entity[] {
  const withImages = entities.filter((e) => e.n_images > 0);
  return withImages.slice().sort((a, b) => {
    const fa = FAMIGLIA_ORDER.indexOf(a.famiglia as EntityFamiglia);
    const fb = FAMIGLIA_ORDER.indexOf(b.famiglia as EntityFamiglia);
    const fai = fa === -1 ? 999 : fa;
    const fbi = fb === -1 ? 999 : fb;
    if (fai !== fbi) return fai - fbi;
    return a.name.localeCompare(b.name, "it");
  });
}
