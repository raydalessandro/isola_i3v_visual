/** @type {import('next').NextConfig} */
//
// next.config.mjs — Step 2 catalogo entità.
//
// Strategia immagini: NON copiamo i ~10MB di immagini in public/. Le serviamo
// dal deploy statico esistente del catalogo (NEXT_PUBLIC_IMAGE_BASE).
// Per Vercel ha senso usare next/image con remotePatterns così l'optimization
// service le ottimizza ed esponiamo solo URL validate.
//
// Cutover (Step finale): basta cambiare NEXT_PUBLIC_IMAGE_BASE a "" o all'URL
// di produzione corretto, oppure sostituire la sorgente con un path locale.

const IMAGE_BASE =
  process.env.NEXT_PUBLIC_IMAGE_BASE || "https://catalogoisola.vercel.app";

let imageRemoteHostname = "";
try {
  imageRemoteHostname = new URL(IMAGE_BASE).hostname;
} catch {
  imageRemoteHostname = "catalogoisola.vercel.app";
}

const nextConfig = {
  reactStrictMode: true,
  images: {
    // path "visual/<categoria>/.../immagini/<file>.jpg" servito dal CDN catalogo.
    remotePatterns: [
      {
        protocol: "https",
        hostname: imageRemoteHostname || "catalogoisola.vercel.app",
        pathname: "/visual/**",
      },
      // host alternativo (cutover di compatibilità)
      {
        protocol: "https",
        hostname: "catalogoisola.vercel.app",
        pathname: "/visual/**",
      },
    ],
  },
};

export default nextConfig;
