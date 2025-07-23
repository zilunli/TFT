import { useState, useEffect } from "react";
import SearchForm from "../components/SearchForm";
import SummonerCard from "../components/SummonerCard";
import { getAccount, getSummoner, getHistory } from "../api/endpoints";

export default function Home() {
  const [query, setQuery] = useState(null);          // { g, t }
  const [account, setAccount] = useState(null);      // account JSON
  const [summoner, setSummoner] = useState(null);    // summoner JSON
  const [history, setHistory] = useState(null);      // match IDs
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState(null);

  // Fire when user submits
  useEffect(() => {
    if (!query) return;
    (async () => {
      try {
        setLoading(true); setErr(null);
        const acc = await getAccount(query.g, query.t);
        setAccount(acc);
        const summ = await getSummoner(acc.puuid);
        setSummoner(summ);
        const ids = await getHistory(acc.puuid, 0, 20);
        setHistory(ids);
      } catch (e) {
        setErr(e);
      } finally {
        setLoading(false);
      }
    })();
  }, [query]);

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-bold">TFT Tools</h1>

      <SearchForm onSubmit={(g, t) => setQuery({ g, t })} />

      {loading && <p>Loading…</p>}
      {err && <p className="text-red-500">Error: {err.message}</p>}

      {summoner && <SummonerCard summoner={summoner} />}
      {history && history.length > 0 && (
        <div>
          <h3 className="font-semibold mt-4">Recent Matches</h3>
          <ul className="list-disc ml-6">
            {history.map(id => <li key={id}>{id}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
}
