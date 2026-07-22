import React from 'react';
import { OrdenCompra, Cotizacion, Cliente } from '../types';
import { PackageCheck, Upload, FileCheck, Clock, CheckCircle } from 'lucide-react';

interface OrdenesCompraViewProps {
  ordenes: OrdenCompra[];
  cotizaciones: Cotizacion[];
  clientes: Cliente[];
  onReceiveOC: (ocId: number, numeroOc: string) => void;
}

export const OrdenesCompraView: React.FC<OrdenesCompraViewProps> = ({
  ordenes,
  cotizaciones,
  clientes,
  onReceiveOC,
}) => {
  const getCotizacionNum = (id: number) =>
    cotizaciones.find((c) => c.id === id)?.numeroCotizacion || 'COT-0000';

  const getClienteName = (cotId: number) => {
    const cot = cotizaciones.find((c) => c.id === cotId);
    if (!cot) return 'Cliente';
    return clientes.find((c) => c.id === cot.clienteId)?.empresa || 'Cliente';
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <PackageCheck className="w-5 h-5 text-indigo-600" />
            Control de Órdenes de Compra (OC)
          </h2>
          <p className="text-xs text-slate-500">
            Seguimiento a la solicitud y recepción formal del soporte presupuestal del cliente.
          </p>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-100 text-slate-600 font-semibold border-b border-slate-200">
              <th className="p-3 pl-4">Cotización</th>
              <th className="p-3">Cliente</th>
              <th className="p-3">Número de OC Cliente</th>
              <th className="p-3">Fecha Solicitud</th>
              <th className="p-3">Estado OC</th>
              <th className="p-3 text-center">Acción</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {ordenes.map((oc) => (
              <tr key={oc.id} className="hover:bg-slate-50 transition-colors">
                <td className="p-3 pl-4 font-bold text-blue-700 font-mono">{getCotizacionNum(oc.cotizacionId)}</td>
                <td className="p-3 font-semibold text-slate-900">{getClienteName(oc.cotizacionId)}</td>
                <td className="p-3 font-mono text-slate-800">{oc.numeroOc || 'Pendiente por cliente'}</td>
                <td className="p-3 text-slate-500">{new Date(oc.fechaSolicitud).toLocaleDateString('es-CO')}</td>
                <td className="p-3">
                  {oc.estado === 'RECIBIDA' ? (
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
                      RECIBIDA
                    </span>
                  ) : (
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-300">
                      SOLICITADA
                    </span>
                  )}
                </td>
                <td className="p-3 text-center">
                  {oc.estado === 'SOLICITADA' && (
                    <button
                      onClick={() => {
                        const num = prompt('Ingrese el número de la Orden de Compra entregada por el cliente:');
                        if (num) onReceiveOC(oc.id, num);
                      }}
                      className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-3 py-1.5 rounded-lg text-xs"
                    >
                      Registrar OC Recibida
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
