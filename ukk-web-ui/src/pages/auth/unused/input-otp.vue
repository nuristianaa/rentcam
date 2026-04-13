<!-- <template>
    <div style="display: flex; flex-direction: row">
      <v-otp-input
        ref="otpInput"
        v-model:value="bindModal"
        input-classes="otp-input"
        separator="-"
        :num-inputs="6"
        :should-auto-focus="true"
        input-type="letter-numeric"
        :conditionalClass="['one', 'two', 'three', 'four', 'five', 'six']"
        :placeholder="['', '', '', '', '', '']"
        @on-change="handleOnChange"
        @on-complete="handleOnComplete"
      />
    </div>
</template>
<script>
import { ref } from 'vue'
// import VOtpInput from 'vue3-otp-input'
export default {
  props: ['modelValue'],
  emits: ['update:modelValue', 'complete'],
  data() {
    return {
      bindModal: ref('')
    }
  },
  methods: {
    handleOnComplete (value) {
      this.$emit('update:modelValue', value)
      this.$emit('complete', 1)
    },
    handleOnChange (value) {
      console.log(value)
    }
  }
}
</script>
<style>
.otp-input {
  width: 40px;
  height: 40px;
  padding: 5px;
  margin: 0 10px;
  font-size: 20px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.3);
  text-align: center;
}
/* Background colour of an input field with value */
.otp-input.is-complete {
  background-color: #e4e4e4;
}
.otp-input::-webkit-inner-spin-button,
.otp-input::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
/* input::placeholder {
  font-size: 15px;
  text-align: center;
  font-weight: 600;
} */
</style> -->
