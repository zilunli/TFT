import React, { useEffect, useState } from "react";
import { getMatch } from "../api/endpoints";
import MatchCard from "./MatchCard";

export default function MatchHistory({ matchIds }) {
  const [matches, setMatches] = useState([]);

  useEffect(() => {
    const fetchMatches = async () => {
      const results = await Promise.all(
        matchIds.map(async (id) => {
          try {
            const res = await getMatch(id)
            return res.data;
          } catch (err) {
            console.error("Failed to fetch match:", id, err);
            return null;
          }
        })
      );
      setMatches(results.filter(Boolean)); // Remove nulls
    };

    fetchMatches();
  }, [matchIds]);

  return (
    <div className="match-list">
      {matches.map((match) => (
        <MatchCard key={match.match_id} match={match} />
      ))}
    </div>
  );
};
