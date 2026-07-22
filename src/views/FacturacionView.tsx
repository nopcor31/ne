import React from 'react';
import { Factura, Cotizacion, Cliente } from '../types';
import { Receipt, DollarSign, CheckCircle2, Clock } from 'lucide-react';

interface FacturacionViewProps {
  facturas: Factura[];
  cotizaciones: Cotizacion[];
  clientes: Cliente[];
  onAddFactura: (factura: Partial<Factura>) => void;
  onPayFactura: (facturaId: number) => void;
}

export const FacturacionView: React.FC<FacturacionViewProps> = ({
  facturas,
  cotizaciones,
  clientes,
  onAddFactura,
  onPayFactura,
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
            <Receipt className="w-5 h-5 text-orange-600" />
            Facturación Electrónica & Cierre Financiero
          </h2>
          <p className="text-xs text-slate-500">
            Módulo final de gestión de cuentas por cobrar, vencimientos de facturas y confirmación de pago.
          </p>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        {facturas.length === 0 ? (
          <div className="p-8 text-center text-xs text-slate-400">
            Sin facturas registradas. Avance cotizaciones a estado "Pendiente Facturación" para generar comprobantes.
          </div>
        ) : (
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-100 text-slate-600 font-semibold border-b border-slate-200">
                <th className="p-3 pl-4">Número Factura</th>
                <th className="p-3">Cotización Referencia</th>
                <th className="p-3">Cliente</th>
                <th className="p-3">Fecha Vencimiento</th>
                <th className="p-3 text-right">Valor Facturado</th>
                <th className="p-3">Estado Pago</th>
                <th className="p-3 text-center">Acción</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {facturas.map((f) => (
                <tr key={f.id} className="hover:bg-slate-50 transition-colors">
                  <td className="p-3 pl-4 font-bold text-slate-900 font-mono">{f.numeroFactura}</td>
                  <td className="p-3 font-bold text-blue-700 font-mono">{getCotizacionNum(f.cotizacionId)}</td>
                  <td className="p-3 font-semibold">{getClienteName(f.cotizacionId)}</td>
                  <td className="p-3 text-slate-500">{f.fechaVencimiento}</td>
                  <td className="p-3 text-right font-black text-slate-900">${f.valorFacturado.toLocaleString('es-CO')}</td>
                  <td className="p-3">
                    {f.estado === 'PAGADA' ? (
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-green-100 text-green-800 border border-green-300">
                        PAGADA
                      </span>
                    ) : (
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-orange-100 text-orange-800 border border-orange-300">
                        PENDIENTE
                      </span>
                    )}
                  </td>
                  <td className="p-3 text-center">
                    {f.estado !== 'PAGADA' && (
                      <button
                        onClick={() => onPayFactura(f.id)}
                        className="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold px-3 py-1.5 rounded-lg text-xs"
                      >
                        Registrar Pago
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};
