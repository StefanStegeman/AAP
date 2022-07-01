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

int main (void)
{
    hwlib::wait_ms(2000);
    hwlib::cout << "Testing and:\t\t" << andTest(10, 7) << " \tNeeds to be: 1" << "\n";
    hwlib::cout << "Testing equals:\t\t" << equals(5, 5) << " \tNeeds to be: 1" << "\n";
    hwlib::cout << "Testing greater:\t" << greater(15, 2) << " \tNeeds to be: 1" << "\n";
    hwlib::cout << "Testing greaterEquals:\t" << greaterEquals(2, 3) << " \tNeeds to be: 0" << "\n";
    hwlib::cout << "Testing if:\t\t" << ifTest(7) << " \tNeeds to be: 1" << "\n";
    hwlib::cout << "Testing less:\t\t" << less(7, 1) << " \tNeeds to be: 0"<< "\n";
    hwlib::cout << "Testing lessEquals:\t" << lessEquals(4, 4) << " \tNeeds to be: 1"<< "\n";
    hwlib::cout << "Testing notEquals:\t" << notEquals(10, 15) <<" \tNeeds to be: 1"<< "\n";
    hwlib::cout << "Testing or:\t\t" << orTest(2, 2)<<" \tNeeds to be: 1"<< "\n";
}