#include "hwlib.hpp"

extern "C" bool andTest(int a, int b);
extern "C" bool equals(int a, int b);
extern "C" bool greater(int a, int b);
extern "C" bool greaterEquals(int a, int b);
extern "C" int ifTest(int a);
extern "C" bool less(int a, int b);
extern "C" bool lessEquals(int a, int b);
extern "C" bool notEquals(int a, int b);
extern "C" bool orTest(int a, int b);
extern "C" bool odd(int n);
extern "C" bool even(int n);
extern "C" int sommig(int n);

int main (void)
{
    hwlib::wait_ms(2000);
    hwlib::cout << "Testing and:\t\t" << andTest(10, 7) << " \tNeeds to be: " << (10 == 10 && 7 == 7) << "\n";
    hwlib::cout << "Testing equals:\t\t" << equals(5, 5) << " \tNeeds to be: " << (5 == 5) << "\n";
    hwlib::cout << "Testing greater:\t" << greater(15, 2) << " \tNeeds to be: " << (15 > 2) << "\n";
    hwlib::cout << "Testing greaterEquals:\t" << greaterEquals(2, 3) << " \tNeeds to be: " << (2 >= 3) << "\n";
    hwlib::cout << "Testing if:\t\t" << ifTest(7) << " \tNeeds to be: " << (7 == 7) << "\n";
    hwlib::cout << "Testing less:\t\t" << less(7, 1) << " \tNeeds to be: "<< (7 < 1) << "\n";
    hwlib::cout << "Testing lessEquals:\t" << lessEquals(4, 4) << " \tNeeds to be: "<< (4 <= 4) << "\n";
    hwlib::cout << "Testing notEquals:\t" << notEquals(10, 15) <<" \tNeeds to be: "<< (10 != 15) << "\n";
    hwlib::cout << "Testing or:\t\t" << orTest(2, 3)<<" \tNeeds to be: "<< (2 != 2 || 3 == 3) << "\n";
    
    hwlib::cout << "Testing odd:\t\t" << odd(3)<<" \tNeeds to be: "<< (3 % 2 != 0) <<"\n";
    hwlib::cout << "Testing even:\t\t" << even(12)<<" \tNeeds to be: "<< (12 % 2 == 0) <<"\n";
    hwlib::cout << "Testing sommig:\t\t" << sommig(12)<<" \tNeeds to be: 78"<<"\n";
}