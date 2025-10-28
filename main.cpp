#include <iostream>
#include <mysql.h>
#include <windows.h>
#include <set>
#include <sstream>
using namespace std;

// Modify as needed
const char* HOST = "localhost";
const char* USER = "root";
const char* PW = "Surajab@218318";
const char* DB = "mydb";
const int TOTAL_BEDS = 5; // Set your hostel bed count

int getReservedBedCount(MYSQL* conn) {
    int reserved = 0;
    if (mysql_query(conn, "SELECT COUNT(*) FROM hostel") == 0) {
        MYSQL_RES* res = mysql_store_result(conn);
        if (res) {
            MYSQL_ROW row = mysql_fetch_row(res);
            if (row) reserved = atoi(row[0]);
            mysql_free_result(res);
        }
    }
    return reserved;
}

void viewAvailableBeds(MYSQL* conn) {
    int reserved = getReservedBedCount(conn);
    cout << "\nAvailable Beds: " << (TOTAL_BEDS - reserved) << "/" << TOTAL_BEDS << endl;
    cout << "Current Allotments:" << endl;
    if (mysql_query(conn, "SELECT BedNo, Name FROM hostel") == 0) {
        MYSQL_RES* res = mysql_store_result(conn);
        MYSQL_ROW row;
        while ((row = mysql_fetch_row(res)) != NULL)
            cout << "  Bed " << row[0] << ": " << row[1] << endl;
        mysql_free_result(res);
    }
    else cout << "  Error reading allotments.\n";
    Sleep(4000);
}

void reserveBed(MYSQL* conn) {
    int reserved = getReservedBedCount(conn);
    if (reserved >= TOTAL_BEDS) {
        cout << "\nSorry! No Bed Available.\n";
        Sleep(2000);
        return;
    }
    string name;
    cout << "\nEnter Student Name: ";
    cin >> name;

    // Find next free bed
    set<int> occupied;
    if (mysql_query(conn, "SELECT BedNo FROM hostel") == 0) {
        MYSQL_RES* res = mysql_store_result(conn);
        MYSQL_ROW row;
        while ((row = mysql_fetch_row(res)) != NULL)
            occupied.insert(atoi(row[0]));
        mysql_free_result(res);
    }
    int bed = -1;
    for (int i = 1; i <= TOTAL_BEDS; ++i) {
        if (occupied.count(i) == 0) {
            bed = i;
            break;
        }
    }
    stringstream ss;
    ss << "INSERT INTO hostel(Name, BedNo) VALUES('" << name << "', " << bed << ")";
    if (mysql_query(conn, ss.str().c_str()) == 0) {
        cout << "Bed " << bed << " reserved for " << name << ".\nPlease pay 5000 Rupees.\n";
    }
    else {
        cout << "Error: " << mysql_error(conn) << endl;
    }
    Sleep(4000);
}

void removeBedAllotment(MYSQL* conn) {
    string name;
    cout << "\nEnter Student Name to Remove: ";
    cin >> name;
    stringstream ss;
    ss << "DELETE FROM hostel WHERE Name = '" << name << "'";
    if (mysql_query(conn, ss.str().c_str()) == 0 && mysql_affected_rows(conn) > 0) {
        cout << "Removed " << name << " from hostel.\n";
    }
    else
        cout << "No such student/allotment found.\n";
    Sleep(2000);
}

int main() {
    MYSQL* conn = mysql_init(NULL);
    if (!mysql_real_connect(conn, HOST, USER, PW, DB, 3306, NULL, 0)) {
        cout << "Error: " << mysql_error(conn) << endl;
        return 1;
    }
    cout << "Logged into Database!" << endl;

    bool exitFlag = false;
    while (!exitFlag) {
        system("cls");
        cout << "\nWelcome To Hostel Management System" << endl;
        cout << "***********************************" << endl;
        cout << "1. View Available Slots" << endl;
        cout << "2. Reserve Bed" << endl;
        cout << "3. Remove Bed Allotment" << endl;
        cout << "4. Exit" << endl;
        cout << "Enter Your Choice: ";
        int choice;
        cin >> choice;
        switch (choice) {
            case 1: viewAvailableBeds(conn); break;
            case 2: reserveBed(conn); break;
            case 3: removeBedAllotment(conn); break;
            case 4: exitFlag = true; cout << "\nGood Luck\n"; Sleep(2000); break;
            default: cout << "\nInvalid Input\n"; Sleep(2000);
        }
    }
    mysql_close(conn);
    return 0;
}
