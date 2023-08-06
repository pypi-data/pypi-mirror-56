import BEM from 'bem.js';

/** @const {string} */
export const BLOCK_DATAGRID = 'datagrid';

/** @aconst {string} */
export const ELEMENT_FILTER = 'filter';

/** @const {NodeList} */
export const DATAGRID_FILTERS = BEM.getBEMNodes(BLOCK_DATAGRID, ELEMENT_FILTER);
