import { useState, useEffect } from "react";
import SearchForm from "../components/SearchForm";
import SummonerCard from "../components/SummonerCard";
import { getAccount, getSummoner, getHistory } from "../api/endpoints";
import MatchHistory from "../components/MatchHistory";

export default function Home() {
  const [query, setQuery] = useState(null);       
  const [account, setAccount] = useState(null);
  const [summoner, setSummoner] = useState(null);
  const [history, setHistory] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState(null);

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
          <h3 className="font-semibold mt-4">Match History</h3>
          <MatchHistory matchIds={history} />
        </div>
      )}
    </div>
  );
}
