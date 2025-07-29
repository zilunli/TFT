import React, { useEffect, useState } from "react";
import { stageMap, rarityMap } from '../types/Static';
import { getQueueType, getTactician } from "../api/endpoints";

export default function MatchCard({ match }) {
    const [duration, setDuration] = useState(null);
    const [queueType, setQueueType] = useState(null);
    const [participantTacticians, setParticipantTacticians] = useState({});

    useEffect(() => {
        function formatDuration(seconds) {
            const totalSeconds = Math.floor(seconds);
            const hrs = Math.floor(totalSeconds / 3600);
            const mins = Math.floor((totalSeconds % 3600) / 60);
            const secs = totalSeconds % 60;

            return [hrs, mins, secs]
            .map((v) => v.toString().padStart(2, '0'))
            .join(':');
        }
        if (match?.info?.game_length) {
            setDuration(formatDuration(match.info.game_length));
        }
    }, [match]);

    useEffect(() => {
        async function fetchQueueType(queueId) {
            try {
                const res = await getQueueType(queueId);
                setQueueType(res.name);  
            } catch (error) {
                console.error("Failed to fetch queue type:", error);
                setQueueType("Unknown");
            }
        }

        if (match?.info?.queue_id) {
            fetchQueueType(match.info.queue_id);
        }
    }, [match]);

    useEffect(() => {
        async function fetchAllTacticians() {
            const tacticianMap = {};
            await Promise.all(match.info.participants.map(async (participant) => {
                try {
                    if (!participant?.companion?.item_ID) {
                        tacticianMap[participant.puuid] = null;
                        return;
                    }
                    const res = await getTactician(participant.companion.item_ID);
                    if (res?.image?.full) {
                        tacticianMap[participant.puuid] = res.image.full;
                    } else {
                        tacticianMap[participant.puuid] = null;
                    }
                } catch (err) {
                    console.error("Failed to fetch tactician for participant", participant.puuid, err);
                    tacticianMap[participant.puuid] = null;
                }
            }));
            setParticipantTacticians(tacticianMap);
        }
        if (match?.info?.participants) {
            fetchAllTacticians();
        }
    }, [match]);

    function calculateBoardValue(units) {
        if (!units || !Array.isArray(units)) return 0;

        return units.reduce((total, unit) => {
            const rarity = unit.rarity;
            const starLevel = unit.tier;
            const cost = rarityMap[rarity];
            const multiplier = starLevel === 3 ? 9 : starLevel === 2 ? 3 : 1;
            return total + cost * multiplier;
        }, 0);
    }

    return (
    <div className="match-card">
        <p>Patch: {match.info.tft_set_core_name}</p>
        <p>Date: {new Date(match.info.game_datetime).toLocaleString('en-US', {
            month: 'short',
            day: '2-digit',
            year: 'numeric'
            })}
        </p>
        <p>Duration: {duration}</p>
        <p>Mode: {queueType}</p>
        <ul>{[...match.info.participants]
            .sort((a, b) => a.placement - b.placement)
            .map((participant, idx) => (
            <li key={idx}>
                <strong>Placement</strong> {participant.placement} — 
                <strong>Name</strong> {participant.riotIdGameName} — 
                <img
                    src={`/assets/tacticians/${participantTacticians[participant.puuid]}`}
                    alt="Tactician"
                    width="100"
                />
                <strong>Level</strong> {participant.level} —  Attached to Tactician Icon 
                <strong>Round Eliminated</strong> {stageMap[participant.last_round]} —
                <strong>Board Value</strong> {calculateBoardValue(participant.units)} —
                <strong>Damage Done</strong> {participant.total_damage_to_players} — 
                <strong>Traits</strong> Function displaying all active traits and tiers — 
                <strong>Units</strong> Function displaying all active units on the board — 
            </li>
            ))}
        </ul>
    </div>
    );
};