// Mapping TFT Stages
export const stageMap: { [key: number]: string } = {};
let roundCounter = 1;
for (let stage = 1; stage <= 8; stage++) {
  for(let round = 1; round <= 7; round++) {
     stageMap[roundCounter] = `${stage}-${round}`;
     roundCounter++
     if (stage === 1 && round === 4) break
  }
}

// Mapping TFT Rarity to Cost
export const rarityMap: { [key: number]: number } = {
  0: 1,
  1: 2,
  2: 3,
  4: 4,
  6: 5
};
