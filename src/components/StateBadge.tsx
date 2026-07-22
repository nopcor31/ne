import React from 'react';
import { EstadoCotizacion } from '../types';
import { ESTADO_COLORS, ESTADO_LABELS } from '../services/stateMachine';

interface StateBadgeProps {
  estado: EstadoCotizacion;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

export const StateBadge: React.FC<StateBadgeProps> = ({ estado, className = '', size = 'md' }) => {
  const colors = ESTADO_COLORS[estado] || { bg: 'bg-gray-100', text: 'text-gray-700', border: 'border-gray-300' };
  const label = ESTADO_LABELS[estado] || estado;

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-xs font-medium',
    lg: 'px-3 py-1.5 text-sm font-semibold',
  }[size];

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border ${colors.bg} ${colors.text} ${colors.border} ${sizeClasses} whitespace-nowrap shadow-xs ${className}`}
    >
      <span className="w-1.5 h-1.5 rounded-full bg-current opacity-75" />
      {label}
    </span>
  );
};
