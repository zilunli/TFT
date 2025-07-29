export default function SummonerCard({ summoner }) {
  return (
    <div className="border p-3 rounded">
      <p>{summoner.profileIconId}</p>
      {/* <h2 className="font-semibold">{account.gameName}</h2> <p>#{account.tagLine}</p> */}
    </div>
  );
}