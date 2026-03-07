"use client";

import SearchBox from "@/components/SearchBox";
import api from "@/utils/api";
import { useQuery } from "@tanstack/react-query";
import { Globe } from "lucide-react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

interface SearchResult {
  title: string;
  summary: string;
  url: string;
}

const SearchPage = () => {
  const query = useSearchParams().get("q") as string;

  const { data } = useQuery({
    queryKey: ["results", query],
    queryFn: async () => {
      const res = await api.get(`/search?q=${encodeURIComponent(query)}`);
      return res.data.results as SearchResult[];
    },
    staleTime: Infinity,
    enabled: !!query,
  });

  return (
    <main>
      <div
        className="-z-10 absolute inset-0 opacity-15"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
        }}
      />
      <div className="flex flex-col gap-3 sm:gap-6 md:gap-8 sm:flex-row items-center sm:items-start px-6 py-8 sm:px-10 md:px-12 md:py-12">
        <div>
          <Link
            href={"/"}
            className="playfair font-light text-xl sm:text-3xl md:text-4xl text-neutral-800/90 leading-tight tracking-tighter text-balance"
          >
            WikiLink
          </Link>
        </div>
        <div className="z-10 w-full md:w-2/4 ">
          <div className="w-full md:w-2/3">
            <SearchBox key={query} defaultVal={query} />
          </div>
          <div className="mt-8">
            {data?.length === 0 ? (
              <p className="text-neutral-500 mt-6">
                No results found for {query}.
              </p>
            ) : (
              data?.map((result, index) => {
                return (
                  <Link
                    href={result.url}
                    rel="noopener noreferrer"
                    key={index}
                    className="cursor-pointer block mb-6 p-4 rounded-none border-b border-b-neutral-300 hover:border-b-neutral-500 transition-colors"
                  >
                    <div className="flex items-center gap-1">
                      <Globe className="inline-block w-4 h-4 text-neutral-500" />
                      <p className="text-xs text-neutral-600">{result.url}</p>
                    </div>
                    <h2 className="hover:underline text-xl mt-2 font-semibold text-green-800">
                      {result.title}
                    </h2>
                    <p className="text-sm text-neutral-700 mt-1">
                      {result.summary}
                    </p>
                  </Link>
                );
              })
            )}
          </div>
        </div>
      </div>
    </main>
  );
};

export default SearchPage;
