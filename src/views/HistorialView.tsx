import React from 'react';
import { HistorialActividad } from '../types';
import { History, Activity, ShieldCheck, User } from 'lucide-react';

interface HistorialViewProps {
  historial: HistorialActividad[];
}

export const HistorialView: React.FC<HistorialViewProps> = ({ historial }) => {
  return (
    <div className="space-y-6">
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <History className="w-5 h-5 text-blue-600" />
            Bitácora de Trazabilidad Transversal (@registrar_historial)
          </h2>
          <p className="text-xs text-slate-500">
            Registro automático inmutable de todas las acciones del usuario y eventos del sistema.
          </p>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 shadow-xs p-6">
        <div className="relative border-l-2 border-slate-200 pl-6 space-y-6 ml-2">
          {historial.map((item) => (
            <div key={item.id} className="relative group">
              {/* Dot */}
              <div className="absolute -left-[31px] top-1.5 w-3.5 h-3.5 rounded-full bg-blue-600 ring-4 ring-white" />

              <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 text-xs space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-900 text-sm">{item.accion}</span>
                  <span className="text-[10px] text-slate-400 font-mono">
                    {new Date(item.fechaHora).toLocaleString('es-CO')}
                  </span>
                </div>

                <p className="text-slate-600">{item.detalle || 'Sin observaciones adicionales'}</p>

                <div className="pt-2 border-t border-slate-200/60 flex items-center gap-2 text-[10px] text-slate-400 font-medium">
                  <span className="flex items-center gap-1">
                    <User className="w-3 h-3 text-slate-500" /> Usuario ID #{item.usuarioId}
                  </span>
                  <span>·</span>
                  <span className="uppercase font-mono bg-slate-200 text-slate-700 px-1.5 py-0.5 rounded">
                    Entidad: {item.entidadTipo} #{item.entidadId}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
