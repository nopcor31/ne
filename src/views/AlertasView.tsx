import React from 'react';
import { Alerta } from '../types';
import { Bell, AlertCircle, AlertTriangle, Info, Check } from 'lucide-react';

interface AlertasViewProps {
  alertas: Alerta[];
  onMarkAsRead: (id: number) => void;
}

export const AlertasView: React.FC<AlertasViewProps> = ({ alertas, onMarkAsRead }) => {
  return (
    <div className="space-y-6">
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Bell className="w-5 h-5 text-rose-600" />
            Centro de Alertas Operativas Proactivas
          </h2>
          <p className="text-xs text-slate-500">
            Avisos generados automáticamente por el hilo secundario (QThread Worker) ante desviaciones del pipeline.
          </p>
        </div>
      </div>

      <div className="space-y-3">
        {alertas.length === 0 ? (
          <div className="p-8 bg-white rounded-xl border border-slate-200 text-center text-xs text-slate-400">
            Sin alertas activas en el sistema.
          </div>
        ) : (
          alertas.map((a) => (
            <div
              key={a.id}
              className={`p-4 rounded-xl border bg-white shadow-xs flex items-start justify-between gap-4 ${
                a.prioridad === 'CRITICA' ? 'border-rose-300' : 'border-amber-300'
              }`}
            >
              <div className="flex items-start gap-3">
                <div className="mt-0.5">
                  {a.prioridad === 'CRITICA' ? (
                    <AlertCircle className="w-5 h-5 text-rose-600" />
                  ) : (
                    <AlertTriangle className="w-5 h-5 text-amber-600" />
                  )}
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-900">{a.titulo}</h4>
                  <p className="text-xs text-slate-600 mt-1">{a.mensaje}</p>
                  <p className="text-[10px] text-slate-400 mt-2 font-mono">
                    Generada: {new Date(a.fechaCreacion).toLocaleString('es-CO')}
                  </p>
                </div>
              </div>

              {!a.fechaVisto && (
                <button
                  onClick={() => onMarkAsRead(a.id)}
                  className="bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold px-3 py-1.5 rounded-lg shrink-0 flex items-center gap-1"
                >
                  <Check className="w-3.5 h-3.5" /> Marcar leída
                </button>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};
