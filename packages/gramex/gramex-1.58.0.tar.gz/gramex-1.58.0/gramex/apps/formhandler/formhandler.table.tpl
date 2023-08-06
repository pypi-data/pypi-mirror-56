<!doctype html>
{% import six %}
{% from formhandler_utils import URLUpdate, SET, ADD, POP, XOR %}
{% set u = URLUpdate(handler.request.uri) %}
{% set _ = globals().get %}
{% set metadata, datasets = (meta, data) if isinstance(data, dict) else ({'data': meta}, {'data': data}) %}
{% set static = '/{}/formhandler-static/node_modules'.format(YAMLURL) %}
<link rel="stylesheet" href="{{ static }}/bootstrap/dist/css/bootstrap.min.css">
<style scoped>
.formhandler-table .table tbody a { color: inherit; }
.formhandler-table-header { display: flex; justify-content: space-between; }
.formhandler-table-modal-form { margin: 0; }
.formhandler-table .col-number, .formhandler-table .col-date { text-align: right; }
</style>
<div class="container-fluid">
  {% for key, dataset in datasets.items() %}
    <div class="formhandler-table">
      {% if _('heading', False) %}
        <h2><a href="?">{{ key }}</a></h2>
      {% end %}
      <div class="formhandler-table-header">
        {% if _('pagination', False) %}
          {% set page = 1 + meta['offset'] // meta['limit'] %}
          {% set last_page = (meta['count'] + meta['limit'] - 1) // meta['limit'] if 'count' in meta else page if len(data) < meta['limit'] else None %}
          {% set lo = max(page - 2, 1) %}
          {% set hi = min(last_page, page + 2) if last_page is not None else page + 2 %}
          <nav aria-label="Table pages">
            <ul class="pagination pagination-sm">
              <li class="page-item{{ ' disabled' if page <= 1 else '' }}">
                <a class="page-link" href="?{{ u(SET, '_offset', meta['offset'] - meta['limit']) }}">Previous</a>
              </li>
              {% if lo > 1 %}
                <li class="page-item">
                  <a class="page-link" href="?{{ u(POP, '_offset') }}">1</a>
                </li>
                {% if lo > 2 %}
                  <li class="page-item disabled"><a class="page-link" href="#">...</a></li>
                {% end %}
              {% end %}
              {% for pg in range(lo, hi + 1) %}
                <li class="page-item{{ ' active' if pg == page else '' }}">
                  <a class="page-link" href="?{{ u(SET, '_offset', meta['limit'] * (pg - 1) or None) }}">{{ pg }}</a>
                </li>
              {% end %}
              {% if 'count' in meta %}
                {% if hi + 1 < last_page %}
                  <li class="page-item disabled"><a class="page-link" href="#">...</a></li>
                {% end %}
                {% if hi < last_page or lo > hi %}
                  <li class="page-item">
                    <a class="page-link" href="?{{ u(SET, '_offset', meta['limit'] * (last_page - 1)) }}">{{ last_page }}</a>
                  </li>
                {% end %}
              {% end %}
              <li class="page-item{{ '' if last_page is None or page < last_page else ' disabled' }}">
                <a class="page-link" href="?{{ u(SET, '_offset', meta['offset'] + meta['limit']) }}">Next</a>
              </li>
              <li class="page-item disabled">&#160;</li>
              <li class="page-item">
                <div class="btn-group btn-group-sm" role="group">
                  {% set limit = metadata[key].get('limit') %}
                  <button id="export-as" type="button" class="btn btn-light btn-sm dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    {{ limit }} rows
                  </button>
                  <div class="dropdown-menu" aria-labelledby="export-as">
                    {% for lim in [10, 20, 50, 100, 200, 500, 1000] %}
                      <a class="dropdown-item{{ ' active' if lim == limit else '' }}" href="?{{ u(SET, '_limit', None if lim == limit else lim) }}">{{ lim }}</a>
                    {% end %}
                  </div>
                </div>
              </li>
              <li class="page-item disabled">&#160;</li>
              <li class="page-item">
                <div class="btn-group btn-group-sm" role="group">
                  <button id="export-as" type="button" class="btn btn-light btn-sm dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Export as
                  </button>
                  <div class="dropdown-menu" aria-labelledby="export-as">
                    {% for fmt in ['xlsx', 'csv', 'json', 'html'] %}
                      <a class="dropdown-item" href="?{{ u(SET, '_format', fmt, SET, '_limit', 10000) }}">{{ fmt.upper() }}</a>
                    {% end %}
                  </div>
                </div>
              </li>
            </ul>
          </nav>
        {% end %}
        {% if _('filters', False) %}
          {% set filter_cols = metadata[key].get('filters', []) %}
          {% set exclude_cols = metadata[key].get('excluded', []) %}
          <span class="formhandler-table-filters">
            {% for col, op, vals in filter_cols %}
              <a href="?{{ u(POP, col + op) }}" class="badge badge-pill badge-dark formhandler-table-filter" title="Clear {{ col + op }} filter">
                {{ col }} {{ op or '=' }} {{ ', '.join(six.text_type(val) for val in vals) }}
              </a>
            {% end %}
            {% for col in exclude_cols %}
              <a href="?{{ u(POP, '_c', '-' + col) }}" class="badge badge-pill badge-dark formhandler-table-filter" title="Show {{ col }} column">
                {{ col }}
              </a>
            {% end %}
            {% if len(filter_cols) or len(exclude_cols) %}
              <a href="{{ handler.request.path }}?_format=table" class="badge badge-pill badge-danger formhandler-table-filter" title="Clear all filters">&times;</a>
            {% end %}
          </span>
        {% end %}
      </div>
      <table class="table table-sm table-striped">
        <thead>
          <tr>
            {% set _sort, _c = u.args.get('_sort', []), u.args.get('_c', []) %}
            {% set _filters = {(col, op): val for col, op, val in meta['filters']} %}
            {% set coltype = {} %}
            {% for colid, col in enumerate(dataset.columns) %}
              {% set dtype = dataset[col].dtype.name %}
              {% set filtername, filters = ('Text', [
                    ('Equals', ''),
                    ('Does not equal', '!'),
                    ('Matches', '~'),
                    ('Does not match', '!~'),
                  ]) if dtype == 'object' else ('Number', [
                    ('Equals', ''),
                    ('Does not equal', '!'),
                    ('Greater than', '>'),
                    ('Less than', '<'),
                  ]) if 'int' in dtype or 'float' in dtype else ('Date', [
                    # TBD
                  ]) if 'datetime' in dtype else ('Other', [
                  ])
              %}
              {% set coltype[col] = filtername.lower() %}
              <th class="{{ 'table-primary' if col in _sort else 'table-active' if '-' + col in _sort else '' }} col-{{ coltype[col] }}">
                <div class="dropdown">
                  <a href="#" class="dropdown-toggle text-nowrap" id="fh-dd-{{ colid }}" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    {{ col }}
                  </a>
                  <div class="dropdown-menu" data-col="{{ col }}" aria-labelledby="dropdownMenuButton">
                    {% if col in _sort %}
                      <a class="dropdown-item active" href="?{{ u(POP, '_sort', col) }}">Sort ascending</a>
                      <a class="dropdown-item" href="?{{ u(POP, '_sort', col, ADD, '_sort', '-' + col) }}">Sort descending</a>
                    {% elif '-' + col in _sort %}
                      <a class="dropdown-item" href="?{{ u( POP, '_sort', '-' + col, ADD, '_sort', col) }}">Sort ascending</a>
                      <a class="dropdown-item active" href="?{{ u(POP, '_sort', '-' + col) }}">Sort descending</a>
                    {% else %}
                      <a class="dropdown-item" href="?{{ u(ADD, '_sort', col) }}">Sort ascending</a>
                      <a class="dropdown-item" href="?{{ u(ADD, '_sort', '-' + col) }}">Sort descending</a>
                    {% end %}
                    <div class="dropdown-divider"></div>
                    <a class="dropdown-header disabled">{{ filtername }} Filters</a>
                    {% for filter_name, filter_op in filters %}
                      {% set vals = _filters.get((col, filter_op), None) %}
                      {% set active = vals is not None and len(vals) %}
                      <a class="dropdown-item{{ ' active' if active else '' }}" href="#"
                        data-toggle="modal"
                        data-target="#formhandler-table-modal-id"
                        data-op="{{ filter_op }}"
                        data-url="?{{ u(SET, col + filter_op, '\t') }}"
                      >{{ filter_name }} {{ '...' if not active or len(vals) > 1 else six.text_type(vals[0]) }}</a>
                    {% end %}
                    <a class="dropdown-item{{ ' active' if len(_filters.get((col, ''), 'xx')) == 0 else '' }}" href="?{{ u(XOR, col, '') }}">Not empty</a>
                    <a class="dropdown-item{{ ' active' if len(_filters.get((col, '!'), 'xx')) == 0 else '' }}" href="?{{ u(XOR, col + '!', '') }}">Empty</a>
                    {% if len(filters) %}
                      <div class="dropdown-divider"></div>
                    {% end %}
                    <a class="dropdown-item" href="">Format...</a>
                    <a class="dropdown-item" href="?{{ u(ADD, '_c', '-' + col) }}">Hide</a>
                  </div>
                </div>
              </th>
            {% end %}
          </tr>
        </thead>
        <tbody>
          {% for index, row in dataset.iterrows() %}
            <tr>
              {% for col in dataset.columns %}
                <td class="col-{{ coltype[col] }}">
                  <a href="?{{ u(ADD, col, row[col]) }}">
                    {{ row[col] }}
                  </a>
                </td>
              {% end %}
            </tr>
          {% end %}
        </tbody>
      </table>
    </div><!-- .formhandler-table -->
  {% end %}
</div><!-- .container-fluid -->

<div class="modal formhandler-table-modal" id="formhandler-table-modal-id" tabindex="-1" role="dialog" aria-labelledby="formhandler-table-modal-label" aria-hidden="true">
  <div class="modal-dialog modal-sm" role="document">
    <div class="modal-content">
      <form class="formhandler-table-modal-form modal-body">
        <label id="formhandler-table-modal-label" for="formhandler-table-modal-value">Value</label>
        <p><input class="form-control" name="value"></p>
        <div>
          <button type="button" class="btn btn-sm btn-secondary" data-dismiss="modal">Cancel</button>
          <button type="submit" class="btn btn-sm btn-primary">Apply filter</button>
          <button type="button" class="btn btn-sm btn-danger remove-action">Remove filter</button>
        </div>
      </form><!-- .modal-body -->
    </div><!-- .modal-content -->
  </div><!-- .modal-dialog -->
</div><!-- .modal -->

<script src="{{ static }}/jquery/dist/jquery.slim.min.js"></script>
<script src="{{ static }}/popper.js/dist/umd/popper.min.js"></script>
<script src="{{ static }}/bootstrap/dist/js/bootstrap.min.js"></script>
<script src="{{ static }}/url-search-params/build/url-search-params.js"></script>
<script>
(function() {
  var u = new URLSearchParams(location.search)
  var current_key
  $('body')
    .on('shown.bs.modal', '.formhandler-table-modal', function(e) {
      var $el = $(e.relatedTarget)
      var op_text = $el.text()
      var op = $el.data('op')
      var col = $el.closest('.dropdown-menu').data('col')
      current_key = col + op
      $('form', this).data('url', $el.data('url'))
      $('label', this).text(col + ' ' + op_text)
      $('input', this).val(u.get(current_key)).focus()
    })
    .on('submit', '.formhandler-table-modal-form', function(e) {
      e.preventDefault()
      u.delete(current_key)
      u.append(current_key, $('input', this).val())
      location.href = '?' + u
    })
    .on('click', '.formhandler-table-modal-form .remove-action', function(e) {
      e.preventDefault
      u.delete(current_key)
      location.href = '?' + u
    })
})()
</script>
