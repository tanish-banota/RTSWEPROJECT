"use client";

import { useState, useMemo, useEffect } from "react";
import { Event } from "@/lib/api";

type SearchFilterProps = {
  events: Event[];
  onFilteredEventsChange: (events: Event[]) => void;
};

export default function SearchFilter({
  events,
  onFilteredEventsChange,
}: SearchFilterProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedTags, setSelectedTags] = useState<string[]>([]);

  // Extract all unique tags from events
  const allTags = useMemo(() => {
    const tags = new Set<string>();
    events.forEach((event) => {
      event.tags?.forEach((tag) => tags.add(tag));
    });
    return Array.from(tags).sort();
  }, [events]);

  // Filter events based on search query and selected tags
  const filteredEvents = useMemo(() => {
    return events.filter((event) => {
      // Search query matches title, club, or description
      const matchesSearch =
        searchQuery === "" ||
        event.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        event.club.toLowerCase().includes(searchQuery.toLowerCase()) ||
        event.description.toLowerCase().includes(searchQuery.toLowerCase());

      // If tags are selected, event must have at least one matching tag
      const matchesTags =
        selectedTags.length === 0 ||
        selectedTags.some((tag) => event.tags?.includes(tag));

      return matchesSearch && matchesTags;
    });
  }, [events, searchQuery, selectedTags]);

  // Update parent with filtered events (use useEffect, not useMemo)
  useEffect(() => {
    onFilteredEventsChange(filteredEvents);
  }, [filteredEvents, onFilteredEventsChange]);

  const toggleTag = (tag: string) => {
    setSelectedTags((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]
    );
  };

  const clearFilters = () => {
    setSearchQuery("");
    setSelectedTags([]);
  };

  return (
    <div className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
      {/* SEARCH BAR */}
      <div className="mb-4">
        <input
          type="text"
          placeholder="Search events by title, club, or description..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* TAG FILTERS */}
      {allTags.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-gray-700 mb-2">
            Filter by Tags:
          </h3>
          <div className="flex flex-wrap gap-2 mb-3">
            {allTags.map((tag) => (
              <button
                key={tag}
                onClick={() => toggleTag(tag)}
                className={`px-3 py-1 rounded-full text-sm transition-colors ${
                  selectedTags.includes(tag)
                    ? "bg-blue-500 text-white"
                    : "bg-white border border-gray-300 text-gray-700 hover:border-blue-500"
                }`}
              >
                {tag}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* FILTER INFO AND CLEAR BUTTON */}
      <div className="flex justify-between items-center text-sm text-gray-600">
        <span>
          {filteredEvents.length} of {events.length} events
          {selectedTags.length > 0 && ` • ${selectedTags.length} tag filter(s)`}
        </span>
        {(searchQuery || selectedTags.length > 0) && (
          <button
            onClick={clearFilters}
            className="text-blue-500 hover:text-blue-700 font-medium"
          >
            Clear filters
          </button>
        )}
      </div>
    </div>
  );
}
