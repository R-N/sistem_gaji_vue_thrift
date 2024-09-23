<template>
    <center-layout column>
        <v-card>
            <reset-password-form :token="token" />
        </v-card>
    </center-layout>
</template>
<script>

import { TUserEmailErrorCode, T_USER_EMAIL_ERROR_STR } from '@/rpc/gen/user.email.errors_types';

import { authRouter } from '@/router/routers/auth';
import stores from "@/store/stores";
import { router } from '@/router/index';

import { Component, Prop } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';

import ResetPasswordForm from '@/modules/email/password/views/form';
import CenterLayout from '@/components/layout/CenterLayout';

@Component({
    name: "ResetPasswordView",
    //beforeRouteEnter: authRouter.routeRequireLogoutNow(),
    components: {
        CenterLayout,
        ResetPasswordForm
    }
})
class ResetPasswordView extends BaseView {

    get token(){
        return this.$route.params.token;
    }

    async mounted(){
        if (!this.token){
            stores.helper.error.showError(
                T_USER_EMAIL_ERROR_STR[TUserEmailErrorCode.RESET_PASSWORD_TOKEN_INVALID], 
                "beranda"
            );
            return;
        }
    }


}
export { ResetPasswordView }
export default ResetPasswordView
</script>

<style scoped>

</style>
