import { expect, test } from 'vitest'
import { TV_CHANNELS, tvChannelSprites } from './tvChannels'

test('channels reuse existing watch/nature actions so mission accounting is preserved', () => {
  expect(TV_CHANNELS.map(c => [c.label, c.action])).toEqual([
    ['BB Sea', 'tv_watch'], ['Sport', 'tv_watch'], ['Nature', 'tv_nature'],
  ])
})

test('higher-tier channel lookup falls back to lower channel art before generic ON art', () => {
  expect(tvChannelSprites('nature', 3)).toEqual([
    'obj_tv_t3_channel_nature_on', 'obj_tv_t2_channel_nature_on', 'obj_tv_channel_nature_on',
  ])
})
