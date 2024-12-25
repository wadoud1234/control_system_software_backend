import control as ctrl
import matplotlib.pyplot as plt

# Define the transfer function (example: H(s) = (s + 1)/(s^2 + 2s + 1))
num = [1, 1]  # Numerator: s + 1
den = [1, -3, 2]  # Denominator: s^2 - 3s + 2

# Create the transfer function
system_tf = ctrl.TransferFunction(num, den)

# Convert the transfer function to state-space form
print(ctrl.tf2ss(system_tf))

# Print the state-space matrices
# print("State-space representation:")
# print("A matrix:", A)
# print("B matrix:", B)
# print("C matrix:", C)
# print("D matrix:", D)
