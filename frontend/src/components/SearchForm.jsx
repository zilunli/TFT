import { useState } from "react";

export default function SearchForm({ onSubmit }) {
  const [gameName, setGame] = useState("");
  const [tagLine, setTag]   = useState("");

  return (
    <form
      className="flex gap-2"
      onSubmit={e => { e.preventDefault(); onSubmit(gameName.trim(), tagLine.trim()); }}
    >
      <input className="border p-1" placeholder="GameName"
             value={gameName} onChange={e => setGame(e.target.value)} />
      <input className="border p-1 w-20" placeholder="Tag"
             value={tagLine} onChange={e => setTag(e.target.value)} />
      <button className="border px-3 py-1" type="submit">Search</button>
    </form>
  );
}
