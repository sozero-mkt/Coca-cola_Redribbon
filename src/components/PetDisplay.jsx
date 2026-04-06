import React from 'react'

// Map of action -> emoji expression (replace src with actual images when available)
const EXPRESSIONS = {
  idle:    { emoji: '😊', label: '평온' },
  eating:  { emoji: '😋', label: '냠냠' },
  inspired:{ emoji: '🤩', label: '영감받음' },
  loved:   { emoji: '🥰', label: '사랑받는 중' },
}

export default function PetDisplay({ expression }) {
  const current = EXPRESSIONS[expression] || EXPRESSIONS.idle

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      marginBottom: '24px',
    }}>
      {/* Character display — swap this <div> with <img> when assets are ready */}
      <div style={{
        width: '160px',
        height: '160px',
        borderRadius: '50%',
        background: 'radial-gradient(circle at 40% 40%, #ff6b6b, #c0392b)',
        border: '4px solid #e60000',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '72px',
        boxShadow: '0 0 32px #e6000055',
        transition: 'all 0.3s ease',
        userSelect: 'none',
      }}>
        {current.emoji}
      </div>
      <span style={{
        marginTop: '10px',
        color: '#ff9999',
        fontSize: '13px',
        fontWeight: '500',
        letterSpacing: '1px',
      }}>
        {current.label}
      </span>
    </div>
  )
}
