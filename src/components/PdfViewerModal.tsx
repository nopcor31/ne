import React from 'react';
import { Cotizacion, Cliente, ContactoCliente, ConfiguracionSistema, Servicio, Ciudad } from '../types';
import { FileText, Download, Mail, X, CheckCircle } from 'lucide-react';

interface PdfViewerModalProps {
  cotizacion: Cotizacion;
  cliente: Cliente | undefined;
  contacto: ContactoCliente | undefined;
  config: ConfiguracionSistema;
  servicios: Servicio[];
  ciudades: Ciudad[];
  onClose: () => void;
  onSendEmail?: () => void;
}

export const PdfViewerModal: React.FC<PdfViewerModalProps> = ({
  cotizacion,
  cliente,
  contacto,
  config,
  servicios,
  ciudades,
  onClose,
  onSendEmail,
}) => {
  const getServicioNombre = (id: number) => servicios.find((s) => s.id === id)?.nombre || 'Servicio Médico';
  const getCiudadNombre = (id: number) => ciudades.find((c) => c.id === id)?.nombre || 'Ciudad';

  return (
    <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50 overflow-y-auto animate-in fade-in duration-200">
      <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl w-full max-w-3xl overflow-hidden my-8">
        {/* Modal Header */}
        <div className="bg-slate-900 text-white p-4 px-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-600 rounded-lg text-white">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">
                Cotización PDF — {cotizacion.numeroCotizacion}
              </h3>
              <p className="text-xs text-slate-300">Vista previa del documento generado por ReportLab PDF Engine</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {onSendEmail && (
              <button
                onClick={onSendEmail}
                className="bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-colors"
              >
                <Mail className="w-3.5 h-3.5" /> Enviar por Outlook
              </button>
            )}
            <button
              onClick={() => alert('PDF descargado en el almacenamiento local.')}
              className="bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-colors"
            >
              <Download className="w-3.5 h-3.5" /> Descargar PDF
            </button>
            <button
              onClick={onClose}
              className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* PDF Document Container */}
        <div className="p-8 bg-slate-100 max-h-[75vh] overflow-y-auto">
          <div className="bg-white rounded-lg p-8 border border-slate-300 shadow-lg font-sans text-slate-800 text-xs space-y-6">
            {/* PDF Document Header */}
            <div className="flex items-start justify-between border-b border-slate-200 pb-6">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <div className="w-7 h-7 bg-blue-600 text-white font-black text-xs flex items-center justify-center rounded">
                    NE
                  </div>
                  <h1 className="text-base font-extrabold text-slate-900 tracking-tight">
                    {config.empresaNombre}
                  </h1>
                </div>
                <p className="text-[11px] text-slate-500">NIT: {config.empresaNit}</p>
                <p className="text-[11px] text-slate-500">{config.empresaDireccion}</p>
                <p className="text-[11px] text-slate-500">Teléfono: {config.empresaTelefono}</p>
              </div>

              <div className="text-right">
                <div className="inline-block bg-slate-900 text-white font-extrabold px-3 py-1 rounded text-sm mb-1">
                  OFERTA ECONÓMICA
                </div>
                <p className="text-xs font-bold text-blue-700">{cotizacion.numeroCotizacion}</p>
                <p className="text-[11px] text-slate-500">
                  Fecha de emisión: {new Date(cotizacion.fechaCreacion).toLocaleDateString('es-CO')}
                </p>
                <p className="text-[11px] text-slate-500">Vigilancia: SuperSalud Colombia</p>
              </div>
            </div>

            {/* Client & Contact Info */}
            <div className="grid grid-cols-2 gap-4 bg-slate-50 p-4 rounded-lg border border-slate-200">
              <div>
                <p className="font-bold text-slate-400 uppercase text-[10px] tracking-wider mb-1">
                  DATOS DEL CLIENTE
                </p>
                <p className="font-bold text-slate-900 text-sm">{cliente?.empresa}</p>
                <p className="text-slate-600">NIT: {cliente?.nit}</p>
                <p className="text-slate-600">Dirección: {cliente?.direccion}</p>
              </div>
              <div>
                <p className="font-bold text-slate-400 uppercase text-[10px] tracking-wider mb-1">
                  ATENCIÓN A
                </p>
                <p className="font-bold text-slate-900">{contacto?.nombre || 'Contacto Principal'}</p>
                <p className="text-slate-600">{contacto?.cargo}</p>
                <p className="text-slate-600">{contacto?.correo}</p>
                <p className="text-slate-600">{contacto?.telefono}</p>
              </div>
            </div>

            {/* Event Desglose Table */}
            <div>
              <h4 className="font-bold text-slate-900 uppercase text-xs mb-2 border-b border-slate-200 pb-1">
                DETALLE DE EVENTOS Y COBERTURA MÉRIDA/AMBULATORIA
              </h4>

              <table className="w-full text-left border-collapse border border-slate-200">
                <thead>
                  <tr className="bg-slate-100 text-slate-700 font-bold border-b border-slate-200">
                    <th className="p-2 border-r border-slate-200">Servicio</th>
                    <th className="p-2 border-r border-slate-200">Fecha / Ciudad</th>
                    <th className="p-2 border-r border-slate-200">Horas (Diurnas / Nocturnas)</th>
                    <th className="p-2 border-r border-slate-200 text-right">Subtotal Horas</th>
                    <th className="p-2 text-right">Total Evento</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 text-[11px]">
                  {cotizacion.eventos.map((ev, i) => (
                    <tr key={ev.id} className="hover:bg-slate-50/50">
                      <td className="p-2 border-r border-slate-200">
                        <p className="font-bold text-slate-900">{getServicioNombre(ev.servicioId)}</p>
                        <p className="text-[10px] text-slate-500">
                          Horario: {ev.horaInicio} a {ev.horaFin} ({ev.tipoDia})
                        </p>
                      </td>
                      <td className="p-2 border-r border-slate-200">
                        <p>{ev.fecha}</p>
                        <p className="text-[10px] text-slate-500">{getCiudadNombre(ev.ciudadId)}</p>
                      </td>
                      <td className="p-2 border-r border-slate-200">
                        <p>{ev.horasDiurnas}h Diurnas</p>
                        <p className="text-[10px] text-slate-500">{ev.horasNocturnas}h Nocturnas</p>
                      </td>
                      <td className="p-2 border-r border-slate-200 text-right">
                        ${(ev.valorHorasDiurnas + ev.valorHorasNocturnas).toLocaleString('es-CO')}
                      </td>
                      <td className="p-2 text-right font-bold text-slate-900">
                        ${ev.valorEvento.toLocaleString('es-CO')}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Financial Summary */}
            <div className="flex justify-end">
              <div className="w-64 bg-slate-50 p-4 rounded-lg border border-slate-200 space-y-1.5 text-xs">
                <div className="flex justify-between text-slate-600">
                  <span>Subtotal Servicios:</span>
                  <span>${cotizacion.valorSubtotal.toLocaleString('es-CO')}</span>
                </div>
                <div className="flex justify-between text-slate-600">
                  <span>Recargos & Extras:</span>
                  <span>${cotizacion.valorExtras.toLocaleString('es-CO')}</span>
                </div>
                <div className="border-t border-slate-300 pt-1.5 flex justify-between font-extrabold text-sm text-slate-900">
                  <span>VALOR TOTAL (COP):</span>
                  <span className="text-blue-700">${cotizacion.valorTotal.toLocaleString('es-CO')}</span>
                </div>
              </div>
            </div>

            {/* Commercial Conditions */}
            <div className="border-t border-slate-200 pt-4 text-[10px] text-slate-500 space-y-1">
              <p className="font-bold text-slate-700 uppercase">CONDICIONES COMERCIALES</p>
              <p className="whitespace-pre-line">{cotizacion.condicionesComerciales || config.pdfCondicionesGenerales}</p>
            </div>

            {/* Footer Signatures */}
            <div className="pt-8 grid grid-cols-2 gap-8 border-t border-slate-200 text-[11px] text-slate-600">
              <div className="border-t border-slate-400 pt-2 text-center">
                <p className="font-bold text-slate-900">SERVICIOS MÉDICOS NE S.A.S.</p>
                <p className="text-[10px] text-slate-500">Coordinación Operativa y Comercial</p>
              </div>
              <div className="border-t border-slate-400 pt-2 text-center">
                <p className="font-bold text-slate-900">{cliente?.empresa}</p>
                <p className="text-[10px] text-slate-500">Aceptación de la Propuesta / Firma y Sello</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
