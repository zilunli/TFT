export default function SummonerCard({ summoner }) {
  return (
    <div className="border p-3 rounded">
      <h2 className="font-semibold">{summoner.name}</h2>
      <p>Level: {summoner.summonerLevel}</p>
      <p>PUUID: {summoner.puuid}</p>
    </div>
  );
}