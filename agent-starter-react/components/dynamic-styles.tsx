'use client'

import { useState, useEffect } from 'react'

interface DynamicStylesProps {
  initialStyles: string
}

export function DynamicStyles({ initialStyles }: DynamicStylesProps) {
  const [mountedStyles, setMountedStyles] = useState('')

  useEffect(() => {
    setMountedStyles(initialStyles)
  }, [initialStyles])

  return mountedStyles ? (
    <style suppressHydrationWarning>{mountedStyles}</style>
  ) : null
}