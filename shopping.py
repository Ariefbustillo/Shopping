import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )
    print(evidence[0])
    print(labels[0])

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    data = ([],[])
    months = {"Jan":0,"Feb":1, "Mar":2,"Apr":3,"May":4,"June":5,"Jul":6,"Aug":7,"Sep":8,"Oct":9,"Nov":10,"Dec":11}
    with open(filename, newline='') as f:
        r = csv.reader(f, delimiter = ',')
        titles = True
        for row in r:
            if(titles == True):
                titles = False
                continue
            colnum = 0
            evidence = []
            label = 0
            for col in row:
                if(colnum == 0 or colnum == 2 or colnum == 4 or (colnum > 10 and colnum < 15)):
                    evidence.append(int(col))
                elif(colnum == 10):
                    evidence.append(int(months[col]))
                elif(colnum == 15):
                    if(col == "Returning_Visitor"):
                        evidence.append(1)
                    else:
                        evidence.append(0)
                elif(colnum == 16):
                    if(col == "TRUE"):
                        evidence.append(1)
                    else:
                        evidence.append(0)
                elif(colnum == 17):
                    if(col == "TRUE"):
                        label = 1
                else:
                    # print(col)
                    evidence.append(float(col))
                colnum += 1
            data[0].append(evidence)
            data[1].append(label)
        return data

                



def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence,labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity_totals = 0
    sensitivity_correct = 0
    specificity_totals = 0
    specificity_correct = 0
    for x in range(len(labels)):
        if(labels[x] == 0):
            specificity_totals += 1
            if(predictions[x] == 0):
                specificity_correct += 1
        elif(labels[x] == 1):
            sensitivity_totals += 1
            if(predictions[x] == 1):
                sensitivity_correct += 1
        else:
            print("ERROR")

    return (sensitivity_correct/sensitivity_totals,specificity_correct/specificity_totals)



if __name__ == "__main__":
    main()
