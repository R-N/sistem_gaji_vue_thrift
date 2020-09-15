<template>
	<main-card title="Profil" no-toolbar="true">
		<template v-slot:default>
			<v-row>
				<v-col lg="6">
					<img class="bg" v-lazy="require('@/assets/img/avatar.png')"/>
				</v-col>
				<v-col lg="6">
					<editable-cell 
						@edit="nameEdit = name"
						@cancel="nameEdit = name"
						@finish="setName()"
						:change-detector="() => name != nameEdit"
						:confirm-text-maker="setNameConfirmText"
						read-only-mode="true"
					>
						<template v-slot:editing="{ readonly }">
							<v-text-field 
								class="bigger-input"
								name="name" 
								v-model="nameEdit" 
								:rules="nameRules"
								:counter="nameLenMax"
								type="email"
								label="Nama"
								:readonly="readonly"
								required
							/>
						</template>
					</editable-cell>
					<editable-cell 
						@edit="emailEdit = email"
						@cancel="emailEdit = email"
						@finish="setEmail()"
						:change-detector="() => email != emailEdit"
						:confirm-text-maker="setEmailConfirmText"
						read-only-mode="true"
					>
						<template v-slot:editing="{ readonly }">
							<v-text-field 
								class="bigger-input"
								name="email" 
								v-model="emailEdit" 
								:rules="emailRules"
								:counter="emailLenMax"
								type="email"
								label="Email"
								:readonly="readonly"
								required
							/>
						</template>
					</editable-cell>
					<div class="d-flex flex-grow-1">
						<v-text-field 
							class="bigger-input"
							label="Role"
							readonly
							:value="roleText"
						/>
					</div>
					<v-form ref="passwordForm" @submit.prevent.stop="setPasswordDialog = true">
						<collapse-transition>
							<div class="d-flex flex-column" v-if="passwordEditing">
									<div class="d-flex flex-grow-1">
										<v-text-field 
											class="bigger-input"
											name="password" 
											v-model="passwordEdit" 
											:rules="passwordRules"
											:counter="passwordLenMax"
											label="Password"
											required
										    :append-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
										    @click:append="() => { passwordVisible = !passwordVisible }"
										    :type="passwordVisible ? 'text' : 'password'"
										/>
									</div>
									<div class="d-flex flex-grow-1">
										<v-text-field 
											class="bigger-input"
											v-model="passwordConfirm" 
											:rules="confirmRules"
											:counter="passwordLenMax"
											label="Konfirmasi Password"
											required
											type="password"
										/>
									</div>
							</div>
						</collapse-transition>
						<fade-transition group class="d-flex flex-grow-1 justify-end">
							<v-btn color="primary" @click="beginPasswordEdit" v-if="!passwordEditing" key="beginPassword">Ubah Password</v-btn>
							<v-btn class="mr-2" @click="cancelPasswordEdit" v-if="passwordEditing" key="cancelPassword">Batal</v-btn>
							<v-btn color="primary" type="submit" v-if="passwordEditing" key="savePassword">Simpan</v-btn>
						</fade-transition>
					</v-form>
				</v-col>
			</v-row>
			<simple-input-dialog 
				v-model="setPasswordDialog" 
				:on-cancel="cancelPasswordEdit"
				:on-confirm="setPassword"
				title="Ubah Password"
				text="Apa Anda yakin password baru sudah benar?"
				:no-input="true"
			/>
		</template>
	</main-card>
</template>

<script>
import { Component, Prop, Watch } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';
import { authRouter } from '@/router/routers/auth';
import stores from "@/store/stores";
import { TUserRole, T_USER_ROLE_STR } from "@/rpc/gen/auth_types";
import { TUserError, TUserErrorCode, T_USER_ERROR_STR, NAME_LEN_MAX, EMAIL_LEN_MAX, PASSWORD_LEN_MAX } from "@/rpc/gen/user_types";
import { router } from "@/router/index";

import MainCard from '@/components/general/MainCard';
import EditableCell from '@/components/general/EditableCell';
import { NAME_RULES, EMAIL_RULES, PASSWORD_RULES } from '@/lib/validators/user';
import {SlideYUpTransition, SlideXLeftTransition, FadeTransition, CollapseTransition} from 'vue2-transitions'
import SimpleInputDialog from '@/components/general/SimpleInputDialog'

@Component({
  	name: "ProfilView",
  	components: {
  		MainCard,
  		EditableCell,
  		SlideYUpTransition,
  		CollapseTransition,
  		SlideXLeftTransition,
  		FadeTransition,
  		SimpleInputDialog
  	},
	beforeRouteEnter: authRouter.routeRequireLoginNow()
})
class ProfilView extends BaseView {
	nameRules = NAME_RULES
	emailRules = EMAIL_RULES
	passwordRules = PASSWORD_RULES

	nameLenMax = NAME_LEN_MAX
	emailLenMax = EMAIL_LEN_MAX
	passwordLenMax = PASSWORD_LEN_MAX

	emailEdit = ''
	nameEdit = ''
	passwordEdit = ''
	passwordConfirm = ''
	passwordVisible = false

	passwordEditing = false;
	setPasswordDialog = false;

	async mounted(){
		stores.app.setBreadcrumbs([
			{ text: "Beranda", to: { name: 'beranda' }, exact: true },
			{ text: "Profil" }
		]);
		this.init();
	}
	clearPassword(){
		this.passwordEdit = '';
		this.passwordConfirm = '';
	}
	init(){
		this.emailEdit = this.email;
		this.nameEdit = this.name;
		this.clearPassword();
	}
	get username(){
		return stores.auth.user.username;
	}
	get email(){
		return stores.auth.user.email;
	}
	get name(){
		return stores.auth.user.name;
	}
	get role(){
		return stores.auth.user.role;
	}
	get roleText(){
		return T_USER_ROLE_STR[this.role];
	}

	beginPasswordEdit(){
		this.clearPassword();
		this.passwordEditing = true;
	}
	cancelPasswordEdit(){
		this.clearPassword();
		this.passwordEditing = false;
		this.setPasswordDialog = false;
	}

	validateConfirm(passwordConfirm){
		if (this.passwordEdit === passwordConfirm) return true;
		return "Konfirmasi tidak sama";
	}
	get confirmRules(){
		return [
			v => !!v || "Konfirmasi tidak boleh kosong",
			this.validateConfirm
		];
	}

	setEmailConfirmText(){
		return "Apa Anda yakin ingin mengubah email menjadi '" 
			+ this.emailEdit + "'?"
	}
	async setEmail(){
		const view = this;
		view.busy=true;
		try{
			if (!view.emailEdit) throw new TUserError({ code: TUserErrorCode.EMAIL_EMPTY});
			await stores.client.user.set_email(view.emailEdit);
		} catch (error) {
			view.handleError(error);
		} finally {
			view.busy = false;
		}
	}

	setNameConfirmText(){
		return "Apa Anda yakin ingin mengubah nama menjadi '" 
			+ this.nameEdit + "'?"
	}
	async setName(){
		const view = this;
		view.busy=true;
		try{
			if (!view.nameEdit) throw new TUserError({ code: TUserErrorCode.NAME_EMPTY});
			await stores.client.user.set_name(view.nameEdit);
		} catch (error) {
			view.handleError(error);
		} finally {
			view.busy = false;
		}
	}

	async setPassword(){
		const view = this;
		view.busy=true;
		try{
			await stores.client.user.set_password(this.passwordEdit);
			this.cancelPasswordEdit();
		} catch (error) {
			this.handleError(error);
		} finally {
			view.busy = false;
		}
	}
	handleError(error){
		if (error instanceof TUserError){
			stores.app.pushTabDialog({
				title: "Error",
				text: T_USER_ERROR_STR[error.code]
			});
		}else{
			throw error;
		}
	}
}
export { ProfilView } 
export default ProfilView
</script>
<style scoped>
</style>
