/** Presentation channels reuse the existing watch/nature actions; no progression rules. */
export const TV_CHANNELS = [
  { id: 'news', label: 'BB Sea', action: 'tv_watch' },
  { id: 'sport', label: 'Sport', action: 'tv_watch' },
  { id: 'nature', label: 'Nature', action: 'tv_nature' },
] as const
export type TvChannel = (typeof TV_CHANNELS)[number]['id']

/** Prefer channel art at this tier, then lower tiers, then the generic ON fallback. */
export function tvChannelSprites(channel: TvChannel, tier = 1): string[] {
  const names: string[] = []
  for (let t = tier; t >= 2; t--) names.push(`obj_tv_t${t}_channel_${channel}_on`)
  return [...names, `obj_tv_channel_${channel}_on`]
}
