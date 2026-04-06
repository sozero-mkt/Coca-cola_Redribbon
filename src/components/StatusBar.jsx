import React from 'react'

const STATUS_COLORS = {
  love: '#ff4d6d',
  energy: '#f4c430',
  vibe: '#6a0dad',
}

const STATUS_LABELS = {
  love: '❤️ 사랑',
  energy: '⚡ 에너지',
  vibe: '✨ 바이브',
}

export default function StatusBar({ label, value }) {
  const color = STATUS_COLORS[label]
  const displayLabel = STATUS_LABELS[label]

  return (
    <div style={{ marginBottom: '12px' }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        marginBottom: '4px',
        color: '#fff',
        fontSize: '14px',
        fontWeight: '600',
      }}>
        <span>{displayLabel}</span>
        <span style={{ color }}>{value} / 100</span>
      </div>
      <div style={{
        background: '#3a0000',
        borderRadius: '20px',
        height: '14px',
        overflow: 'hidden',
        border: '1px solid #5a0000',
      }}>
        <div style={{
          width: `${value}%`,
          height: '100%',
          background: `linear-gradient(90deg, ${color}aa, ${color})`,
          borderRadius: '20px',
          transition: 'width 0.4s ease',
        }} />
      </div>
    </div>
  )
}
