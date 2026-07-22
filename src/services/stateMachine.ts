import { EstadoCotizacion } from '../types';

export interface TransitionRule {
  from: EstadoCotizacion;
  to: EstadoCotizacion[];
  actionLabel: string;
  requiredFields?: string[];
}

export const TRANSITION_MAP: Record<EstadoCotizacion, EstadoCotizacion[]> = {
  [EstadoCotizacion.BORRADOR]: [EstadoCotizacion.COTIZADA],
  [EstadoCotizacion.COTIZADA]: [EstadoCotizacion.ENVIADA_CLIENTE],
  [EstadoCotizacion.ENVIADA_CLIENTE]: [
    EstadoCotizacion.ACEPTADA_CLIENTE,
    EstadoCotizacion.RECHAZADA_CLIENTE,
  ],
  [EstadoCotizacion.ACEPTADA_CLIENTE]: [EstadoCotizacion.PENDIENTE_AREA_MEDICA],
  [EstadoCotizacion.RECHAZADA_CLIENTE]: [EstadoCotizacion.BORRADOR], // Duplicar como nuevo borrador
  [EstadoCotizacion.PENDIENTE_AREA_MEDICA]: [
    EstadoCotizacion.APROBADA_AREA_MEDICA,
    EstadoCotizacion.RECHAZADA_CLIENTE,
  ],
  [EstadoCotizacion.APROBADA_AREA_MEDICA]: [EstadoCotizacion.PROGRAMADA],
  [EstadoCotizacion.PROGRAMADA]: [EstadoCotizacion.OC_SOLICITADA],
  [EstadoCotizacion.OC_SOLICITADA]: [EstadoCotizacion.OC_RECIBIDA],
  [EstadoCotizacion.OC_RECIBIDA]: [EstadoCotizacion.PENDIENTE_FACTURACION],
  [EstadoCotizacion.PENDIENTE_FACTURACION]: [EstadoCotizacion.FACTURADA],
  [EstadoCotizacion.FACTURADA]: [EstadoCotizacion.PAGADA],
  [EstadoCotizacion.PAGADA]: [EstadoCotizacion.CERRADA],
  [EstadoCotizacion.CERRADA]: [],
};

export const ESTADO_LABELS: Record<EstadoCotizacion, string> = {
  [EstadoCotizacion.BORRADOR]: 'Borrador',
  [EstadoCotizacion.COTIZADA]: 'Cotizada',
  [EstadoCotizacion.ENVIADA_CLIENTE]: 'Enviada a Cliente',
  [EstadoCotizacion.ACEPTADA_CLIENTE]: 'Aceptada por Cliente',
  [EstadoCotizacion.RECHAZADA_CLIENTE]: 'Rechazada por Cliente',
  [EstadoCotizacion.PENDIENTE_AREA_MEDICA]: 'Pendiente Área Médica',
  [EstadoCotizacion.APROBADA_AREA_MEDICA]: 'Aprobada Área Médica',
  [EstadoCotizacion.PROGRAMADA]: 'Programada',
  [EstadoCotizacion.OC_SOLICITADA]: 'OC Solicitada',
  [EstadoCotizacion.OC_RECIBIDA]: 'OC Recibida',
  [EstadoCotizacion.PENDIENTE_FACTURACION]: 'Pendiente Facturación',
  [EstadoCotizacion.FACTURADA]: 'Facturada',
  [EstadoCotizacion.PAGADA]: 'Pagada',
  [EstadoCotizacion.CERRADA]: 'Cerrada',
};

export const ESTADO_COLORS: Record<EstadoCotizacion, { bg: string; text: string; border: string }> = {
  [EstadoCotizacion.BORRADOR]: { bg: 'bg-slate-100', text: 'text-slate-700', border: 'border-slate-300' },
  [EstadoCotizacion.COTIZADA]: { bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-300' },
  [EstadoCotizacion.ENVIADA_CLIENTE]: { bg: 'bg-purple-50', text: 'text-purple-700', border: 'border-purple-300' },
  [EstadoCotizacion.ACEPTADA_CLIENTE]: { bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-300' },
  [EstadoCotizacion.RECHAZADA_CLIENTE]: { bg: 'bg-rose-50', text: 'text-rose-700', border: 'border-rose-300' },
  [EstadoCotizacion.PENDIENTE_AREA_MEDICA]: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-300' },
  [EstadoCotizacion.APROBADA_AREA_MEDICA]: { bg: 'bg-teal-50', text: 'text-teal-700', border: 'border-teal-300' },
  [EstadoCotizacion.PROGRAMADA]: { bg: 'bg-cyan-50', text: 'text-cyan-700', border: 'border-cyan-300' },
  [EstadoCotizacion.OC_SOLICITADA]: { bg: 'bg-indigo-50', text: 'text-indigo-700', border: 'border-indigo-300' },
  [EstadoCotizacion.OC_RECIBIDA]: { bg: 'bg-sky-50', text: 'text-sky-700', border: 'border-sky-300' },
  [EstadoCotizacion.PENDIENTE_FACTURACION]: { bg: 'bg-orange-50', text: 'text-orange-700', border: 'border-orange-300' },
  [EstadoCotizacion.FACTURADA]: { bg: 'bg-lime-50', text: 'text-lime-700', border: 'border-lime-300' },
  [EstadoCotizacion.PAGADA]: { bg: 'bg-green-100', text: 'text-green-800', border: 'border-green-400' },
  [EstadoCotizacion.CERRADA]: { bg: 'bg-gray-200', text: 'text-gray-800', border: 'border-gray-400' },
};

export function esTransicionValida(actual: EstadoCotizacion, nuevo: EstadoCotizacion): boolean {
  const permitidos = TRANSITION_MAP[actual] || [];
  return permitidos.includes(nuevo);
}

export function obtenerProximosEstados(actual: EstadoCotizacion): EstadoCotizacion[] {
  return TRANSITION_MAP[actual] || [];
}
