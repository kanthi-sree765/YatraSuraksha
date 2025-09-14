pragma solidity ^0.8.0;

contract TouristIDRegistry {
    struct TouristID {
        string digitalIdHash;
        uint timestamp;
    }

    mapping(address => TouristID) public registry;

    function registerTourist(string memory _digitalIdHash) public {
        registry[msg.sender] = TouristID(_digitalIdHash, block.timestamp);
    }

    function getDigitalIdHash(address _tourist) public view returns (string memory) {
        return registry[_tourist].digitalIdHash;
    }
}
