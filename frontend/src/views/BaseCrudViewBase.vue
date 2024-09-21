
<script>
import stores from "@/store/stores";

import { Component, Prop, Watch, Model } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';

@Component({
    name: "BaseCrudViewBase",
  	components: {
  	}
})
class BaseCrudViewBase extends BaseView {
    createDialog = false;
    search = ''
    items = []

    get nameField() { return "nama"; }
    get itemNameLower(){ return 'item'; }
    get client(){ return null; }
    get headers(){ return []; }
    get breadcrumbs() { return []; }
    get query(){ return {}; }
    get filteredErrors() { return []; }

    _deleteConfirmText(item){
        return `Apa Anda yakin ingin menghapus ${this.itemNameLower} '${item[this.nameField]}'?`;
    }

    async _askDelete(item, ask){
        if (ask)
            ask();
    }

    async _deleteItem(item, releaseBusy=true){
        const view = this;
        view.busy=true;
        try{
            await this.client.delete(item.id);
            this.items.pop(item);
        } catch (error) {
            view.showError(error);
        } finally {
            if (releaseBusy)
                view.busy = false;
        }
    }

    async _mounted(){
        await stores.app.setBreadcrumbs(this.breadcrumbs);
        await this.fetch();
    }

    async _fetch(releaseBusy=true){
        const view = this;
        view.busy = true;
        let query = this.query;
        try{
            let items = await this.client.fetch(query);
            this.items = items;
        } catch(error){
            view.showError(error);
        } finally {
            if (releaseBusy)
                view.busy = false;
        }
    }
    _setNamaConfirmText(item, newValue){
        return setFieldConfirmText("nama", item, newValue);
    }

    async _setNama(item, newValue){
        return await this.setField("nama", item, newValue);
    }

    _setFieldConfirmText(fieldName, item, newValue, alias=null){
        let oldValue = item[fieldName];
        // let newValue = item[newField];
        if (alias){
            oldValue = alias[oldValue];
            newValue = alias[newValue];
        }
        return `Apa Anda yakin ingin mengubah ${fieldName} ${this.itemNameLower} '${item[this.nameField]}' dari '${oldValue}' menjadi '${newValue}'?`
    }
    async _setField(fieldName, item, value, releaseBusy=true){
        const view = this;
        view.busy=true;
        try{
            await this.client[`set_${fieldName}`](item.id, value);
            item[fieldName] = value;
        } catch (error) {
            view.showError(error);
        } finally {
            if (releaseBusy)
                view.busy = false;
        }
    }

    _setEnabledConfirmText(item){
        return this.toggleFieldConfirmText("enabled", 'menonaktifkan', 'mengaktifkan', item);
    }

    async _setEnabled(item, enabled){
        return await this.toggleField("enabled", item, enabled);
    }

    _toggleFieldConfirmText(fieldName, disable, enable, item){
        let action = item[fieldName] ? disable : enable;
        return `Apa Anda yakin ingin ${action} ${this.itemNameLower} '${item[this.nameField]}'?`;
    }

    async _toggleField(toggleName, item, enabled){
        if (enabled === undefined || enabled === null)
            enabled = !item.enabled;
        return await this.setField(toggleName, item, enabled);
    }

    _showError(error){
        if (stores.helper.error.showFilteredError(error, this.filteredErrors)) 
            return;
        throw error;
    }

    
    deleteConfirmText(item){
        return this._deleteConfirmText(item);
    }

    async askDelete(item, ask){
        return await this._askDelete(item, ask);
    }

    async deleteItem(item, releaseBusy=true){
        return await this._deleteItem(item, releaseBusy);
    }

    async mounted(){
        return await this._mounted();
    }

    async fetch(releaseBusy=true){
        return await this._fetch(releaseBusy=true);
    }
    setNamaConfirmText(item){
        return this._setNamaConfirmText(item);
    }

    async setNama(item, nama){
        return await this._setNama(item, nama);
    }

    setFieldConfirmText(fieldName, item, newValue, alias=null){
        return this._setFieldConfirmText(fieldName, item, newValue, alias);
    }

    async setField(fieldName, item, value, releaseBusy=true){
        return await this._setField(fieldName, item, value, releaseBusy);
    }

    setEnabledConfirmText(item){
        return this._setEnabledConfirmText(item);
    }

    async setEnabled(item, enabled){
        return await this._setEnabled(item, enabled);
    }

    toggleFieldConfirmText(fieldName, disable, enable, item){
        return this._toggleFieldConfirmText(fieldName, disable, enable, item);
    }

    async toggleField(toggleName, item, enabled){
        return await this._toggleField(toggleName, item, enabled);
    }

    showError(error){
        return this._showError(error);
    }
}
export { BaseCrudViewBase } 
export default BaseCrudViewBase
</script>