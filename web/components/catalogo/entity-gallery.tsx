"use client";

import * as React from "react";
import Image from "next/image";
import { Download } from "lucide-react";

import type { EntityImage } from "@/lib/types";
import { imageUrl, imageDownloadUrl, imageBasename } from "@/lib/image-url";
import { Lightbox } from "@/components/catalogo/lightbox";

interface EntityGalleryProps {
  images: EntityImage[];
  altPrefix: string;
}

export function EntityGallery({ images, altPrefix }: EntityGalleryProps) {
  const [openIndex, setOpenIndex] = React.useState<number | null>(null);

  // WI-2: download sequenziale per evitare jszip come dipendenza.
  // Il browser scarica un file alla volta; il proxy /api/img force
  // l'attachment lato server (WI-3) anche per origini cross.
  const downloadAll = React.useCallback(() => {
    images.forEach((img, i) => {
      setTimeout(() => {
        const a = document.createElement("a");
        a.href = imageDownloadUrl(img.path);
        a.download = imageBasename(img.path);
        document.body.appendChild(a);
        a.click();
        a.remove();
      }, i * 350); // sfasamento per non sommergere il browser
    });
  }, [images]);

  if (images.length === 0) return null;

  return (
    <section aria-label="Galleria immagini" className="space-y-3">
      <header className="flex items-center justify-between gap-3">
        <p className="font-mono text-xs uppercase tracking-wider text-ink-soft">
          {images.length} {images.length === 1 ? "immagine" : "immagini"}
        </p>
        {images.length > 1 && (
          <button
            type="button"
            onClick={downloadAll}
            className="inline-flex items-center gap-1.5 rounded-md border border-rule px-3 py-1.5 font-mono text-xs uppercase tracking-wider text-ink-soft hover:border-accent/40 hover:text-accent"
          >
            <Download className="h-3.5 w-3.5" aria-hidden />
            Scarica tutte
          </button>
        )}
      </header>
      <ul className="grid grid-cols-2 gap-2 sm:grid-cols-3 md:grid-cols-4">
        {images.map((img, i) => (
          <li key={img.path}>
            <button
              type="button"
              aria-label={`Apri immagine ${i + 1} di ${images.length}: ${img.filename}`}
              onClick={() => setOpenIndex(i)}
              className="group relative block aspect-square w-full overflow-hidden rounded-md border border-rule-soft bg-rule-soft/30 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
            >
              <Image
                src={imageUrl(img.path)}
                alt={`${altPrefix} — ${img.filename}`}
                fill
                sizes="(max-width: 640px) 50vw, (max-width: 768px) 33vw, 25vw"
                className="object-cover transition-transform duration-300 group-hover:scale-[1.03]"
                loading={i === 0 ? "eager" : "lazy"}
                unoptimized
              />
              <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-ink/80 to-transparent p-2 opacity-0 transition-opacity group-hover:opacity-100">
                <span className="font-mono text-[10px] text-paper truncate block">
                  {img.filename}
                </span>
              </div>
            </button>
          </li>
        ))}
      </ul>
      {openIndex != null && (
        <Lightbox
          images={images}
          index={openIndex}
          onClose={() => setOpenIndex(null)}
          onIndexChange={setOpenIndex}
        />
      )}
    </section>
  );
}
