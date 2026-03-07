"use client";

import { Search } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState } from "react";

const SearchBox = ({ defaultVal }: { defaultVal?: string }) => {
  const [searchQuery, setSearchQuery] = useState<string>(defaultVal || "");
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim() === "") return;
    router.push(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
  };

  return (
    <form onSubmit={handleSearch} className="w-full">
      <div className="relative">
        <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-neutral-500 pointer-events-none" />
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search Wikipedia..."
          className="playfair w-full rounded-full border-2 border-neutral-400 text-neutral-800 placeholder-neutral-500 py-3 pl-10 pr-4 text-sm sm:text-base focus:outline-none focus:border-white focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-neutral-600 transition-all"
          aria-label="Wikipedia search input"
        />
      </div>
    </form>
  );
};

export default SearchBox;
