import React, { useState, useCallback } from 'react'
import StatusBar from './components/StatusBar'
import PetDisplay from './components/PetDisplay'

const INITIAL_STATUS = {
  love: 50,
  energy: 80,
  vibe: 30,
}

const ACTIONS = [
  { type: 'EAT',      label: '밥 주기',    emoji: '🍔' },
  { type: 'INSPIRE',  label: '영감 주기',  emoji: '🎵' },
  { type: 'LOVE',     label: '사랑 표현',  emoji: '💖' },
]

// How long the expression lingers after an action (ms)
const EXPRESSION_DURATION = 2000

export default function App() {
  const [status, setStatus] = useState(INITIAL_STATUS)
  const [expression, setExpression] = useState('idle')

  const triggerExpression = useCallback((expr) => {
    setExpression(expr)
    setTimeout(() => setExpression('idle'), EXPRESSION_DURATION)
  }, [])

  const handleAction = useCallback((type) => {
    setStatus((prev) => {
      switch (type) {
        case 'EAT':
          triggerExpression('eating')
          return { ...prev, energy: Math.min(100, prev.energy + 20) }
        case 'INSPIRE':
          triggerExpression('inspired')
          return { ...prev, vibe: Math.min(100, prev.vibe + 25) }
        case 'LOVE':
          triggerExpression('loved')
          return { ...prev, love: Math.min(100, prev.love + 15) }
        default:
          return prev
      }
    })
  }, [triggerExpression])

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #1a0000 0%, #3a0000 50%, #1a0000 100%)',
    }}>
      <div style={{
        width: '360px',
        background: '#2a0000cc',
        border: '1px solid #5a0000',
        borderRadius: '24px',
        padding: '32px 28px',
        boxShadow: '0 8px 40px #00000088',
      }}>
        {/* Header */}
        <h1 style={{
          textAlign: 'center',
          color: '#ff4444',
          fontSize: '20px',
          fontWeight: '700',
          marginBottom: '24px',
          letterSpacing: '2px',
          textTransform: 'uppercase',
        }}>
          🎀 Red Ribbon
        </h1>

        {/* Pet character with expression */}
        <PetDisplay expression={expression} />

        {/* Status bars */}
        <div style={{ marginBottom: '28px' }}>
          {Object.entries(status).map(([key, value]) => (
            <StatusBar key={key} label={key} value={value} />
          ))}
        </div>

        {/* Action buttons */}
        <div style={{
          display: 'flex',
          gap: '10px',
          justifyContent: 'center',
        }}>
          {ACTIONS.map(({ type, label, emoji }) => (
            <button
              key={type}
              onClick={() => handleAction(type)}
              style={{
                flex: 1,
                padding: '12px 8px',
                background: 'linear-gradient(180deg, #cc0000, #990000)',
                border: '1px solid #ff4444',
                borderRadius: '14px',
                color: '#fff',
                fontSize: '12px',
                fontWeight: '600',
                cursor: 'pointer',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: '4px',
                transition: 'transform 0.1s, box-shadow 0.1s',
              }}
              onMouseDown={(e) => { e.currentTarget.style.transform = 'scale(0.95)' }}
              onMouseUp={(e) => { e.currentTarget.style.transform = 'scale(1)' }}
              onMouseLeave={(e) => { e.currentTarget.style.transform = 'scale(1)' }}
            >
              <span style={{ fontSize: '22px' }}>{emoji}</span>
              <span>{label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
