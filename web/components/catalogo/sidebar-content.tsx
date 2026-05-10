"use client";

import * as React from "react";
import Link from "next/link";
import { Map, BookOpen } from "lucide-react";

import type { Tree } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { SearchBox } from "@/components/catalogo/search-box";
import { SidebarTree } from "@/components/catalogo/sidebar-tree";

interface SidebarContentProps {
  tree: Tree;
  totalEntities: number;
}

/** Contenuto interno della sidebar (riutilizzato sia in desktop che in drawer). */
export function SidebarContent({ tree, totalEntities }: SidebarContentProps) {
  const [query, setQuery] = React.useState("");
  return (
    <div className="flex h-full flex-col">
      <div className="border-b border-rule-soft px-4 py-4 space-y-3">
        <div className="flex items-center justify-between">
          <Link
            href="/catalogo"
            className="font-serif text-lg font-semibold text-ink hover:text-accent"
          >
            Catalogo
          </Link>
          <Badge variant="secondary" className="font-mono text-[10px]">
            {totalEntities} entità
          </Badge>
        </div>
        <SearchBox value={query} onChange={setQuery} />
      </div>

      <div className="min-h-0 flex-1 overflow-y-auto px-2 py-3">
        <SidebarTree tree={tree} query={query} />
      </div>

      <div className="border-t border-rule-soft p-4 space-y-2">
        <p className="font-mono text-[10px] uppercase tracking-wider text-ink-faint">
          In arrivo (Step 3)
        </p>
        <div className="space-y-1">
          <DisabledLink icon={Map} label="Indice strade" />
          <DisabledLink icon={BookOpen} label="Storie del libro" />
        </div>
        <Separator className="my-2" />
        <Link
          href="/"
          className="font-mono text-[11px] text-ink-faint hover:text-accent"
        >
          ← Home cruscotto
        </Link>
      </div>
    </div>
  );
}

function DisabledLink({
  icon: Icon,
  label,
}: {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
}) {
  return (
    <div
      aria-disabled="true"
      className="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-ink-faint cursor-not-allowed"
      title="Disponibile in Step 3"
    >
      <Icon className="h-4 w-4 shrink-0" />
      <span className="truncate">{label}</span>
      <span className="ml-auto font-mono text-[9px] uppercase tracking-wider opacity-70">
        soon
      </span>
    </div>
  );
}
