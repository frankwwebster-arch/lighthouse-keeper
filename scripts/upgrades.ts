/**
 * npm run upgrades
 *
 * Reads data/upgrades.csv (the upgrade list Frank and Codex fill in) and writes
 * the game's copy to src/game/upgrades.data.ts. A test fails if the two differ.
 */
import { readFileSync, writeFileSync } from 'node:fs'
import { upgradeRows } from '../src/game/csv.ts'

const rows = upgradeRows(readFileSync('data/upgrades.csv', 'utf8'))
const out = `// Made by \`npm run upgrades\` from data/upgrades.csv. Edit the CSV, not this file.
import type { UpgradeRow } from './csv'

export const UPGRADE_ROWS: readonly UpgradeRow[] = [
${rows.map((r) => `  ${JSON.stringify(r)},`).join('\n')}
]
`
writeFileSync('src/game/upgrades.data.ts', out)
console.log(`${rows.length} upgrade rows written to src/game/upgrades.data.ts`)
