import React from 'react';
import { EstadoCotizacion } from '../types';
import { Check } from 'lucide-react';

interface ProgressStepsProps {
  currentEstado: EstadoCotizacion;
}

const PIPELINE_ORDER = [
  { estado: EstadoCotizacion.BORRADOR, label: 'Borrador' },
  { estado: EstadoCotizacion.COTIZADA, label: 'Cotizada' },
  { estado: EstadoCotizacion.ENVIADA_CLIENTE, label: 'Enviada' },
  { estado: EstadoCotizacion.ACEPTADA_CLIENTE, label: 'Aceptada' },
  { estado: EstadoCotizacion.PENDIENTE_AREA_MEDICA, label: 'Área Médica' },
  { estado: EstadoCotizacion.APROBADA_AREA_MEDICA, label: 'Aprobada Méd.' },
  { estado: EstadoCotizacion.PROGRAMADA, label: 'Programada' },
  { estado: EstadoCotizacion.OC_SOLICITADA, label: 'OC Solicitada' },
  { estado: EstadoCotizacion.OC_RECIBIDA, label: 'OC Recibida' },
  { estado: EstadoCotizacion.PENDIENTE_FACTURACION, label: 'Facturación' },
  { estado: EstadoCotizacion.FACTURADA, label: 'Facturada' },
  { estado: EstadoCotizacion.PAGADA, label: 'Pagada' },
  { estado: EstadoCotizacion.CERRADA, label: 'Cerrada' },
];

export const ProgressSteps: React.FC<ProgressStepsProps> = ({ currentEstado }) => {
  const isRechazada = currentEstado === EstadoCotizacion.RECHAZADA_CLIENTE;
  const currentIndex = PIPELINE_ORDER.findIndex((step) => step.estado === currentEstado);

  return (
    <div className="w-full overflow-x-auto py-2">
      <div className="min-w-[800px] flex items-center justify-between">
        {PIPELINE_ORDER.map((step, idx) => {
          const isPassed = !isRechazada && idx < currentIndex;
          const isCurrent = !isRechazada && idx === currentIndex;

          return (
            <div key={step.estado} className="flex flex-col items-center flex-1 relative">
              {/* Connector line */}
              {idx > 0 && (
                <div
                  className={`absolute top-4 left-[-50%] right-[50%] h-0.5 z-0 ${
                    idx <= currentIndex && !isRechazada ? 'bg-blue-600' : 'bg-slate-200'
                  }`}
                />
              )}

              {/* Step circle */}
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold z-10 transition-all ${
                  isCurrent
                    ? 'bg-blue-600 text-white ring-4 ring-blue-100 shadow-md scale-110'
                    : isPassed
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-100 text-slate-400 border border-slate-300'
                }`}
              >
                {isPassed ? <Check className="w-4 h-4" /> : idx + 1}
              </div>

              {/* Label */}
              <span
                className={`mt-2 text-[11px] text-center font-medium leading-tight max-w-[70px] ${
                  isCurrent
                    ? 'text-blue-700 font-bold'
                    : isPassed
                    ? 'text-slate-700'
                    : 'text-slate-400'
                }`}
              >
                {step.label}
              </span>
            </div>
          );
        })}
      </div>

      {isRechazada && (
        <div className="mt-3 p-2.5 bg-rose-50 border border-rose-200 text-rose-700 rounded-lg text-xs font-medium text-center">
          ⚠️ Cotización rechazada por el cliente. Se puede duplicar para generar un nuevo borrador corregido.
        </div>
      )}
    </div>
  );
};
