import { useState } from 'react'
import { Search, CalendarDays, Clock3, MapPin, Info } from 'lucide-react'
import './PublicRouteSearch.css'

function PublicRouteSearch() {
  const [submitted, setSubmitted] = useState(false)

  function handleSubmit(event) {
    event.preventDefault()
    setSubmitted(true)
  }

  return (
    <section className="public-search" id="buscar" aria-labelledby="public-search-title">
      <div className="public-search__intro">
        <span className="public-search__eyebrow">Consulta pública</span>
        <h2 id="public-search-title">Busca el horario de recolección</h2>
        <p>Selecciona un barrio para consultar los días y la franja horaria prevista.</p>
      </div>

      <form className="public-search__form" onSubmit={handleSubmit}>
        <label className="public-search__field">
          <span><MapPin size={17} aria-hidden="true" /> Barrio</span>
          <input name="barrio" type="text" placeholder="Escribe el nombre del barrio" required />
        </label>

        <label className="public-search__field">
          <span><CalendarDays size={17} aria-hidden="true" /> Día</span>
          <select name="dia" defaultValue="">
            <option value="">Cualquier día</option>
            <option>Lunes</option><option>Martes</option><option>Miércoles</option>
            <option>Jueves</option><option>Viernes</option><option>Sábado</option><option>Domingo</option>
          </select>
        </label>

        <label className="public-search__field">
          <span><Clock3 size={17} aria-hidden="true" /> Franja horaria</span>
          <select name="franja" defaultValue="">
            <option value="">Cualquier franja</option>
            <option>Mañana</option><option>Tarde</option><option>Noche</option>
          </select>
        </label>

        <button className="public-search__submit" type="submit">
          <Search size={18} aria-hidden="true" /> Buscar
        </button>
      </form>

      <p className="public-search__notice">
        <Info size={17} aria-hidden="true" /> Los horarios que se muestren durante el prototipo son datos de prueba y no representan una programación oficial.
      </p>

      <p className="public-search__updated">
        <Clock3 size={16} aria-hidden="true" />
        <span><strong>Actualización:</strong> no hay datos cargados en este prototipo.</span>
      </p>

      {submitted && (
        <div className="public-search__empty" role="status" aria-live="polite">
          <span className="public-search__empty-icon"><CalendarDays size={22} aria-hidden="true" /></span>
          <div>
            <h3>Sin horarios disponibles</h3>
            <p>No hay una programación de prueba para esta búsqueda. Vuelve a intentarlo más adelante.</p>
          </div>
        </div>
      )}
    </section>
  )
}

export default PublicRouteSearch
