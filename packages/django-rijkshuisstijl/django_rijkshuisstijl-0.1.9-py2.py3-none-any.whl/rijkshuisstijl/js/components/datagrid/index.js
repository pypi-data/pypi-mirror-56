//jshint ignore:start
import {DATAGRID_FILTERS} from './constants';

// Start!
if (DATAGRID_FILTERS.length) {
    import(/* webpackChunkName: 'datagrid-filter' */ './datagrid-filter');
}
