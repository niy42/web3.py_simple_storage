// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract simpleStorage {
    uint256 num;

    struct People {
        uint256 num;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public stringtonumb;

    function store(uint256 _num) public {
        num = _num;
    }

    function retrieve() public view returns (uint256) {
        return num;
    }

    function addPeople(string memory _name, uint256 _num) public {
        people.push(People(_num, _name));
        stringtonumb[_name] = _num;
    }
}
