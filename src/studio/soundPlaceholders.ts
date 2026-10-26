import placeholders from '../../data/studio/sound_placeholders.json'

export interface SoundPlaceholder {
  id: string
  label: string
  description: string
  scope: string
}

/**
 * Named sounds that need to be available for authoring before a recipe owns
 * their final runtime cue. Uploading a file with the same id fills the
 * placeholder without changing future recipes or travel-state wiring.
 */
export const SOUND_PLACEHOLDERS = placeholders as readonly SoundPlaceholder[]
export const SOUND_PLACEHOLDER_IDS = SOUND_PLACEHOLDERS.map((placeholder) => placeholder.id)
