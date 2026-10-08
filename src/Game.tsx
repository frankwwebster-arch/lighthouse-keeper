import App from './App'
import { SpriteProvider } from './ui/Sprite'

export default function Game() {
  return (
    <SpriteProvider>
      <App />
    </SpriteProvider>
  )
}
