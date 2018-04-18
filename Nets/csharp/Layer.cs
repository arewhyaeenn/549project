using UnityEngine;

class Layer
{
    public Net master;
    public int node_count;

    public float[] inputs;
    public float[] outputs;
    public float[] differentials;
    public List<float[,]> weights;

    private delegate void Activation();
    public Activation activate;

    private float bound; // bound for relu, log and exp activators
    private float leakiness; // leakiness for sigmoid, relu, log, and exp activators = minimum differential
    private float ln_bound; // to avoid having to recalculate log(bound) for log and exp activators

    public Layer (Net master, string activation, int node_count, float bound=10f, float leakiness)
    {
        this.master = master;

        this.node_count = node_count;
        inputs = new float[node_count];
        outputs = new float[node_count];
        differentials = new float[node_count];

        switch (activation)
        {
            case ("Sigmoid"):
                activate = sigmoid_activate;
                this.leakiness = leakiness;
                break;
            case ("ReLU"):
                activate = relu_activate;
                this.bound = bound;
                this.leakiness = leakiness;
                break;
            case ("Logarithmic"):
                activate = log_activate;
                this.bound = bound;
                this.ln_bound = Mathf.Log(bound);
                this.leakiness = leakiness;
                break;
            case ("Exponential"):

                break;
            default:
                break;
        }
    }

    public void add_value_at_index(float value, int index)
    {
        inputs[index] += value;
    }

    public void reset_inputs()
    {
        inputs = new float[node_count];
    }

    public void sigmoid_activate()
    {
        int i = 0;
        while (i < node_count)
        {
            outputs[i] = 1 / (1 + Mathf.Exp(-inputs[i]));
            differentials[i] = Mathf.Max(outputs[i] * (1 - outputs[i]), leakiness);
            i++;
        }
    }

    public void relu_activate()
    {
        int i = 0;
        while (i < node_count)
        {
            float input = inputs[i];
            if (input > bound)
            {
                outputs[i] = bound;
                differentials[i] = leakiness;
            }
            else if (inputs > 0)
            {
                outputs[i] = inputs;
                differentials[i] = 1;
            }
            else
            {
                outputs[i] = 0;
                differentials[i] = leakiness;
            }
            i++;
        }
    }

    public void log_activate()
    {
        int i = 0;
        while (i < node_count)
        {
            float input = inputs[i];
            if (inputs > bound)
            {
                outputs[i] = ln_bound + 2 - Mathf.Exp(-input / bound + 1);
                differentials[i] = Mathf.Max((ln_bound + 2 - outputs[i]) / bound, leakiness);
            }
            else if (x > 1)
            {
                outputs[i] = Mathf.Log(input);
                differentials[i] = 1 / input;
            }
            else
            {
                outputs[i] = Mathf.Exp(input - 1);
                differentials[i] = Mathf.Max(outputs[i], leakiness);
            }
            i++;
        }
    }

    public void exp_activate()
    {
        int i = 0;
        while(i < node_count)
        {
            float input = inputs[i];
            if (input > ln_bound)
            {
                outputs[i] = 2 - Mathf.Exp(ln_bound - input);
                differentials = Mathf.Max(2 - outputs[i], leakiness);
            }
            else
            {
                outputs[i] = Mathf.Exp(input) / bound;
                differentials[i] = Mathf.Max(outputs[i], leakiness);
            }
            i++;
        }
    }
}