'use client'

import dynamic from 'next/dynamic'
import '../../../studio/studio.css'
import '../../../activityStories/stories.css'

// Bubble stories play in the browser, so the page is never drawn on the server.
const StoryStudio = dynamic(() => import('../../../activityStories/StoryStudio'), { ssr: false })

export default function Page() {
  return <StoryStudio />
}
