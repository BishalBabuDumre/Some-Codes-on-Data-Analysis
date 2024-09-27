import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
def clean_and_process_data(x_values, y_values):
    # Step 1: Remove points with negative y values
    x_filtered, y_filtered = zip(*[(x, y) for x, y in zip(x_values, y_values) if y >= 0])
    
    # Step 2: Remove last three points from the data for calculation
    x_filtered, y_filtered = x_filtered[:-2], y_filtered[:-2]
    
    # Step 3: Calculate the first and second derivatives
    dy_dx = np.gradient(y_filtered, x_filtered)  # First derivative
    d2y_dx2 = np.gradient(dy_dx, x_filtered)     # Second derivative
    #print(d2y_dx2)
    # Step 4: Find where the second derivative changes sign
    sign_change_index = None
    for i in range((len(d2y_dx2)-1), 1, -1):
        if np.sign(d2y_dx2[i]) != np.sign(d2y_dx2[i - 1]):
            sign_change_index = i
            break
    if sign_change_index is not None:
        # Step 5: Remove all points before the sign change and add the point where sign changed
        #print(sign_change_index)
        x_final = list(x_filtered[:(sign_change_index+2)])
        y_final = list(y_filtered[:(sign_change_index+2)])
    else:
        # If no sign change found, return the data as is
        x_final = list(x_filtered)
        y_final = list(y_filtered)
    return x_final, y_final
# Example usage
input_file = "2024-08-19.csv"
df = pd.read_csv(input_file)
volts = df["volts_curve"].tolist()
curr = df["amps_curve"].tolist()

#Reverse part
x = volts[108]
y = curr[108]
x = x[1:]
x = x[:(len(x)-1)]
y = y[1:]
y = y[:(len(y)-1)]
x = list(x.split(","))
y = list(y.split(","))   
abc = 0
x_values = []
y_values = []
for _ in x:
    aa = float(x[abc])
    bb = float(y[abc])
    x_values.append(aa)
    y_values.append(bb)
    abc+=1
# Call the function
x_final, y_final = clean_and_process_data(x_values, y_values)
k = []
for j in y_final:
    j = j*(-1)
    k.append(j)
y_final = k
x_final = list(x_final[-20:]) 
y_final = list(y_final[-20:])
p = x_final[len(x_final)-1]
aa = []
for kk in x_final:
    kk = kk - p
    aa.append(kk)
x_final = aa

#Forward Part. Here, reverse and forward part are taking within 5 minutes of time where
#it is assumed that the irradiation is constant.
#In one time, one  of the cells in the module was partially shaded, whereas
#in another time, it was totally lit.
m = volts[109]
n = curr[109]
m = m[1:]
m = m[:(len(m)-1)]
n = n[1:]
n = n[:(len(n)-1)]
m = list(m.split(","))
n = list(n.split(","))   
pqr = 0
x_valuesF = []
y_valuesF = []
for _ in m:
    aa = float(m[pqr])/96
    bb = float(n[pqr])*(-1)
    x_valuesF.append(aa)
    y_valuesF.append(bb)
    pqr+=1
aaa = 0
nli = []
for _ in y_valuesF:
    ee = y_valuesF[aaa] + abs(y_valuesF[0]-y_final[(len(y_final)-1)])
    nli.append(ee)
    aaa+=1
y_valuesF = nli

#Reverse part II
x = volts[110]
y = curr[110]
x = x[1:]
x = x[:(len(x)-1)]
y = y[1:]
y = y[:(len(y)-1)]
x = list(x.split(","))
y = list(y.split(","))   
abc = 0
x_values = []
y_values = []
for _ in x:
    aa = float(x[abc])
    bb = float(y[abc])
    x_values.append(aa)
    y_values.append(bb)
    abc+=1
# Call the function
x_final2, y_final2 = clean_and_process_data(x_values, y_values)
k = []
for j in y_final2:
    j = j*(-1)
    k.append(j)
y_final2 = k
x_final2 = list(x_final2[-20:]) 
y_final2 = list(y_final2[-20:])
p = x_final2[len(x_final2)-1]
aa = []
for kk in x_final2:
    kk = kk - p
    aa.append(kk)
x_final2 = aa

aaa = 0
nli = []
for _ in y_final2:
    ee = y_final2[aaa] - abs(y_final2[(len(y_final)-1)]-y_final[(len(y_final)-1)])
    nli.append(ee)
    aaa+=1
y_final2 = nli

#plotting both forward and reverse sections
plt.figure()
plt.plot(x_final, y_final, c = 'g', ls = "-", lw = 1.5, label = 'Reverse Horizontal Quarter (2:50 pm)')
plt.plot(x_final2, y_final2, c = 'b', ls = "-.", lw = 1.5, label = 'Reverse Vertical Quarter (3:00 pm)')
plt.plot(x_valuesF, y_valuesF, c = 'r', ls = "--", lw = 1.5, label = 'Forward (2:55 pm)')
plt.legend(loc='upper left', bbox_to_anchor=(0, 1.02), fontsize=8, frameon = False, columnspacing=1.25,handlelength=3)
plt.title('Reverse Bias Characteristics (Aug 19, 2024)', fontsize = 20, fontweight = "bold")
plt.ylabel('Current (A)' , fontsize = 15)
plt.xlabel('Voltage (V)' , fontsize = 15)
plt.grid('on')
plt.xticks(rotation='vertical', fontsize = 8)
plt.tight_layout()
plt.savefig('Curve.png')
plt.close()
