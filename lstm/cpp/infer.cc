#include <stdio.h>
#include <cstdlib>
#include <vector>
#include "tensorflow/lite/interpreter.h"
#include "tensorflow/lite/kernels/register.h"
#include "tensorflow/lite/model.h"
#include "tensorflow/lite/tools/gen_op_registration.h"

int main(){

    std::unique_ptr<tflite::FlatBufferModel> model = tflite::FlatBufferModel::BuildFromFile("model.tflite");

    if(!model){
        printf("Failed to mmap model\n");
        exit(0);
    }

    tflite::ops::builtin::BuiltinOpResolver resolver;
    std::unique_ptr<tflite::Interpreter> interpreter;
    tflite::InterpreterBuilder(*model.get(), resolver)(&interpreter);

    // Resize input tensors, if desired.
    interpreter->AllocateTensors();

    // Dummy tensor input for testing
    // dimensions 1, 120, 1, dtype float32

    srand(0);
    std::vector<std::vector<std::vector<float>>> tensor;
    for (int i = 0; i < 1; ++i) {
        for (int j = 0; j < 120; j++) {
            for (int k = 0; k < 1; k++) {
               tensor[i][j][k] = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
            }
        }
    }

    int input = interpreter->inputs()[0];
    float* input_data_ptr = interpreter->typed_input_tensor<float>(input);
    for (int i = 0; i < 1; ++i) {
        for (int j = 0; j < 120; j++) {
            for (int k = 0; k < 1; k++) {
               *(input_data_ptr) = (float)tensor[i][j][k];
                input_data_ptr++;
            }
        }
    }

    interpreter->Invoke();

    float* output = interpreter->typed_output_tensor<float>(0);

    printf("Result is: %f\n", *output);

    return 0;
}