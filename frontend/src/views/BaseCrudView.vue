<template>
	<main-card :title="title">
		<template v-slot:toolbar-left>
			<icon-button
				@click="create"
				:disabled="busy"
				icon="mdi-plus"
				:text="createText"
				:small="false"
			/>
			<icon-button
				@click="fetch"
				:disabled="busy"
				icon="mdi-refresh"
				:text="refreshText"
				:small="false"
			/>
            <slot name="toolbar-left" :busy="busy"></slot>
		</template>
		<template v-slot:toolbar-right>
            <slot name="toolbar-right" :busy="busy"></slot>
			<v-text-field
                v-if="!(typeof search === 'undefined' || search === null)"
				class="pt-0 mt-0"
				v-model="mySearch"
				append-icon="mdi-magnify"
				label="Search"
				single-line
				hide-details
				:disabled="busy"
			></v-text-field>
		</template>
		<template v-slot:content>
            <slot name="content" :busy="busy"></slot>
		</template>
		<template v-slot:default>
            <slot name="default" :busy="busy"></slot>
		</template>
	</main-card>
</template>

<script>

import { Component, Prop, Watch, Model } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';

import MainCard from '@/components/card/MainCard';
import IconButton from '@/components/button/IconButton';

let modelEvent = "change"

@Component({
    name: "BaseCrudView",
  	components: {
        MainCard,
		IconButton
  	}
})
class BaseCrudView extends BaseView {
    @Prop({default: 'Crud'}) title;
    @Prop({default: 'Buat'}) createText;
    @Prop({default: 'Refresh'}) refreshText;
    @Prop(Function) create;
    @Prop(Function) fetch;
	@Model(modelEvent, { type: [String, Object] }) search;
	
	get mySearch(){
		return this.search;
	}
	set mySearch(value){
		this.$emit(modelEvent, value);
	}
}
export { BaseCrudView } 
export default BaseCrudView
</script>
