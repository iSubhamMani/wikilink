import SearchBox from "@/components/SearchBox";
import { AuroraBackground } from "@/components/ui/aurora";

export default function Home() {
  return (
    <AuroraBackground showRadialGradient={true} animationSpeed={15}>
      <div
        className="absolute inset-0 opacity-15"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
        }}
      />
      <main className="relative min-h-screen flex overflow-hidden">
        <div className="relative z-10 flex flex-col mx-auto justify-center gap-4 px-6 w-full max-w-2xl text-center pb-12">
          {/* Logo */}
          {/* Added a custom drop-shadow to make the text pop forward and glow slightly */}
          <h1 className="playfair font-light text-6xl sm:text-7xl md:text-9xl text-neutral-800/90 leading-tight tracking-tighter text-balance drop-shadow-lg">
            WikiLink
          </h1>

          {/* Subtitle */}
          {/* Added a subtle drop shadow to maintain readability against the horizon glow */}
          <p className="mb-8 text-green-800 text-sm sm:text-lg md:text-xl font-light tracking-wide text-balance drop-shadow-md">
            The minimalist gateway to human knowledge.
          </p>

          {/* Search Box Container */}
          {/* Wrapped the search box in a div with a deep, dark drop-shadow to push it forward off the screen */}
          <div className="relative w-full ">
            <SearchBox />
          </div>
        </div>
      </main>
    </AuroraBackground>
  );
}
